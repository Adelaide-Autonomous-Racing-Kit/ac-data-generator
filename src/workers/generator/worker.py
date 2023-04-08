import multiprocessing as mp
import shutil
from typing import Dict

from src.workers.base import BaseWorker, WorkerSharedState
from src.workers.generator import depth, normals, segmentation

DATA_GENERATORS = {
    "depth": depth.DepthMapGenerator,
    "normals": normals.NormalMapGenerator,
    "segmentation": segmentation.SegmentationGenerator,
}


class DataGenerationWorker(BaseWorker):
    """
    Generates ground truth training data from recordings captured
        using the asseto corsa interface.

    :param configuration: A dictionary containing the configuration information.
    :type configuration: Dict
    :param shared_state: A shared state object to communicate with the main process.
    :type shared_state: WorkerSharedState
    """

    def __init__(self, configuration: Dict, shared_state: WorkerSharedState):
        super().__init__(configuration, shared_state)
        self._data_generators = []

    def _is_work_complete(self) -> bool:
        """
        Check if all work has been completed.

        :return: True if all work has been completed, otherwise False.
        :rtype: bool
        """
        return self.is_ray_casting_done and self._job_queue.empty()

    def _do_work(self):
        """
        Perform the data generation work.
        """
        self._save_ground_truth_data()
        self.increment_n_complete()

    def _save_ground_truth_data(self):
        """
        For each of the registered data generators, generate and save data.
        """
        [data_generator.generate() for data_generator in self._data_generators]
        self._copy_frame()

    def _copy_frame(self):
        """
        Copy the records captured game frame to the output directory.
        """
        filename = self._record_number + ".jpeg"
        source_path = self.recording_path.joinpath(filename)
        destination_path = self.output_path.joinpath(filename)
        shutil.copyfile(source_path, destination_path)

    @property
    def _job_queue(self) -> mp.Queue:
        """
        Get queue that this worker receives jobs from.

        :return: The queue this worker receives jobs from.
        :rtype: mp.Queue
        """
        return self.generation_queue

    @property
    def _record_number(self) -> str:
        """
        Get the current record's id number.

        :return: The current record's id number.
        :rtype: str
        """
        return self._work["record_number"]

    def _setup(self):
        """
        Setup steps specific to the data generation worker.
        """
        self._setup_scene()
        self._setup_data_generators()
        self.set_as_ready()

    def _setup_data_generators(self):
        """
        For each type of data specified in the configuration instance a
            generator for that type.
        """
        for data_type in self._config["generate"]:
            self._add_data_generator(data_type)

    def _add_data_generator(self, data_type: str):
        """
        For a given data type to be generated by the worker create and register
            it to the object.

        :param data_type: The type of data to be generated.
        :type data_type: str
        """
        data_generator = DATA_GENERATORS[data_type](self)
        self._data_generators.append(data_generator)
