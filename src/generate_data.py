import ctypes
import multiprocessing as mp
import time
from pathlib import Path
from typing import List

from halo import Halo
from loguru import logger
from prettytable import PrettyTable
from src.workers import (
    BaseWorker,
    DataGenerationWorker,
    RayCastingWorker,
    SharedState,
    WorkerSharedState,
)
from src.utils.load import load_yaml
from src.utils.records import get_sample_list
from src.utils.save import maybe_create_folders
from tqdm import tqdm


class MultiprocessDataGenerator:
    def __init__(self, configuration_path: str):
        self._setup(configuration_path)

    @property
    def output_path(self) -> Path:
        return Path(self._config["output_path"])

    @property
    def n_ray_casting_workers(self) -> int:
        return self._config["n_ray_casting_workers"]

    @property
    def n_generation_workers(self) -> int:
        return self._config["n_generation_workers"]

    @property
    def recording_path(self) -> Path:
        return Path(self._config["recorded_data_path"])

    @property
    def workers(self) -> List[BaseWorker]:
        return [*self._ray_casting_workers, *self._generation_workers]

    def start(self):
        """
        Runs through each of the records specified in the configuration file
            posting them to the pool of workers. For each record workers can
            generate and save the following:
                - Visualised segmentation map
                - Segmentation map with train ids
                - Visualised normal map of the scene
                - Visualised depth map of the scene
            A copy of the original frame captured is made to the output folder
            to be used as input in training datasets.
        """
        self._start_worker_processes()
        self._wait_until_workers_are_initialised()
        self._monitor_progress()
        self._wait_until_workers_are_done()
        self._clean_up()
        self._log_success()

    def _populate_ray_cast_queue(self):
        [self._shared.ray_cast_queue.put(record) for record in self._records]

    def _start_worker_processes(self):
        [worker.start() for worker in self.workers]
        self._start_time = time.time()

    def _wait_until_workers_are_initialised(self):
        with Halo(text="Waiting until workers are ready...", spinner="line"):
            while not self._is_worker_pool_ready():
                time.sleep(0.1)
        logger.success("Workers initialised")

    def _is_worker_pool_ready(self):
        return all([worker.is_ready for worker in self.workers])

    def _monitor_progress(self):
        self._start_progress_bar()
        while not self._shared.ray_cast_queue.empty():
            self._update_progress_bar()
            time.sleep(0.2)

    def _start_progress_bar(self):
        self._pbar = tqdm(total=len(self._records))

    def _update_progress_bar(self):
        current_n_done = self._shared.n_complete.value
        self._pbar.update(current_n_done - self._last_n_complete)
        self._last_n_complete = current_n_done

    def _wait_until_workers_are_done(self):
        self._wait_until_ray_casters_are_done()
        self._wait_until_generators_are_done()

    def _wait_until_ray_casters_are_done(self):
        with Halo(text="Waiting until ray casters finish...", spinner="line"):
            while not self._is_ray_casting_done():
                time.sleep(0.1)
        self._shared.is_ray_casting_done.value = True

    def _is_ray_casting_done(self) -> bool:
        workers = self._ray_casting_workers
        return all([worker.is_done for worker in workers])

    def _wait_until_generators_are_done(self):
        with Halo(text="Waiting until generators finish...", spinner="line"):
            while not self._is_generation_done():
                time.sleep(0.1)

    def _is_generation_done(self) -> bool:
        workers = self._generation_workers
        return all([worker.is_done for worker in workers])

    def _clean_up(self):
        self._finalise_progress_bar()
        self._terminate_workers()

    def _finalise_progress_bar(self):
        self._update_progress_bar()
        self._pbar.close()

    def _terminate_workers(self):
        [worker.terminate() for worker in self.workers]

    def _log_success(self):
        elapsed = time.time() - self._start_time
        elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        n_records = len(self._records)
        logger.success(f"Generated {n_records} samples in {elapsed} hh:mm:ss")

    def _setup(self, configuration_path: str):
        self._load_config(configuration_path)
        self._setup_folders()
        self._initialise_member_variables()
        self._initialise_shared_state()
        self._log_configuration()
        self._setup_workers()
        self._setup_work()

    def _load_config(self, configuration_path: str):
        self._config = load_yaml(configuration_path)

    def _log_configuration(self):
        table = PrettyTable(["Name", "Setting"])
        self._add_setting_to_table(table)
        self._add_data_generation_to_table(table)
        logger.info("\n" + str(table))

    def _add_setting_to_table(self, table: PrettyTable):
        for key in self._config.keys():
            if key == "generate":
                continue
            table.add_row([key, self._config[key]])

    def _add_data_generation_to_table(self, table: PrettyTable):
        for data_type in self._config["generate"].keys():
            to_generate = ", ".join(self._config["generate"][data_type])
            table.add_row([data_type, to_generate])

    def _setup_work(self):
        self._records = self._get_records_to_be_processed()
        [self._shared.ray_cast_queue.put(record) for record in self._records]

    def _get_records_to_be_processed(self):
        return self._get_subsample()

    def _get_subsample(self):
        start = self._config["start_at_sample"]
        end = self._config["finish_at_sample"]
        interval = self._config["sample_every"]
        samples = get_sample_list(self.recording_path)
        return samples[start:end:interval]

    def _setup_folders(self):
        maybe_create_folders(self.output_path)

    def _initialise_member_variables(self):
        self.is_ready = False
        self._last_n_complete = 0

    def _initialise_shared_state(self):
        self._shared = SharedState(
            ray_cast_queue=mp.Queue(),
            generation_queue=mp.Queue(),
            n_complete=mp.Value("i", 0),
            is_ray_casting_done=mp.Value(ctypes.c_bool, False),
        )

    def _setup_workers(self):
        self._ray_casting_workers = self._create_ray_casting_workers()
        self._generation_workers = self._create_generation_workers()

    def _create_ray_casting_workers(self) -> List[RayCastingWorker]:
        n_workers = self.n_ray_casting_workers
        logger.info(f"Creating {n_workers} ray casting worker(s)...")
        return self._create_workers(n_workers, RayCastingWorker)

    def _create_generation_workers(self) -> List[DataGenerationWorker]:
        n_workers = self.n_generation_workers
        logger.info(f"Creating {n_workers} generation worker(s)...")
        return self._create_workers(n_workers, DataGenerationWorker)

    def _create_workers(
        self,
        n_workers: int,
        constructor: callable,
    ) -> List[BaseWorker]:
        return [self._create_worker(constructor) for _ in range(n_workers)]

    def _create_worker(self, constructor: callable) -> BaseWorker:
        shared_state = self._create_shared_worker_state()
        return constructor(self._config, shared_state)

    def _create_shared_worker_state(self) -> WorkerSharedState:
        shared_state = WorkerSharedState(
            ray_cast_queue=self._shared.ray_cast_queue,
            generation_queue=self._shared.generation_queue,
            is_ray_casting_done=self._shared.is_ray_casting_done,
            is_done=mp.Value(ctypes.c_bool, False),
            is_ready=mp.Value(ctypes.c_bool, False),
            n_complete=self._shared.n_complete,
        )
        return shared_state
