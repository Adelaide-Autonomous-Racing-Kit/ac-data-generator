import abc
from dataclasses import dataclass
import multiprocessing as mp
from pathlib import Path
import queue
from typing import Dict, List

from src.workers.utils import load_track_mesh

QUEUE_TIMEOUT = 0.5


@dataclass
class SharedState:
    """
    A dataclass containing the state shared between all workers in the
        MultiprocessDataGenerator.

    :param ray_cast_queue: The mp queue containing data for the ray casting
        workers.
    :type ray_cast_queue: mp.Queue
    :param generation_queue: The mp queue containing data for the data
        generation workers.
    :type generation_queue: mp.Queue
    :param is_ray_casting_done: The mp Value indicating whether the ray casting
        worker has completed all work.
    :type is_ray_casting_done: mp.Value
    :param n_complete: The mp Value representing the number of tasks completed
        globally, across all workers.
    :type n_complete: mp.Value
    """

    ray_cast_queue: mp.Queue
    generation_queue: mp.Queue
    is_ray_casting_done: mp.Value
    n_complete: mp.Value


@dataclass
class WorkerSharedState(SharedState):
    """
    A dataclass containing the state shared between all workers in the
        MultiprocessDataGenerator in addition to worker specific state.

    :param is_done: A mp Value indicating whether the worker has completed all
        of its assigned work.
    :type is_done: mp.Value
    :param is_ready: A mp Value indicating whether the worker is ready to
        relieve work.
    :type is_ready: mp.Value
    """

    is_done: mp.Value
    is_ready: mp.Value


class BaseWorker(mp.Process):
    """
    A base class for all worker processes.

    :param configuration: A dictionary containing the configuration for the
        worker.
    :type configuration: dict
    :param shared_state: An object containing the shared state between all
        workers in the MultiprocessDataGenerator.
    :type shared_state: WorkerSharedState
    """

    def __init__(self, configuration: Dict, shared_state: WorkerSharedState):
        super().__init__()
        self._config = configuration
        self._shared_state = shared_state

    def run(self):
        """
        The main function that is called when a worker is started. The process
            receives work from a shared mp queue and completes it.
        """
        self._setup()
        self.is_running = True
        while self.is_running:
            self._maybe_do_work()
        self.set_as_done()

    def _maybe_do_work(self):
        """
        Check if there's work available and if there is do it.
        """
        if self._maybe_receive_work():
            self._do_work()

    def _maybe_receive_work(self) -> bool:
        """
        Try to receive work from the job queue.

        :return: True if work was relieved, False otherwise.
        :rtype: bool
        """
        try:
            self._work = self._job_queue.get(timeout=QUEUE_TIMEOUT)
            return True
        except queue.Empty:
            if self._is_work_complete():
                self.is_running = False
            return False

    @abc.abstractmethod
    def _do_work(self):
        """
        Implementation specific to the type of worker being derived

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _setup(self):
        """
        Specific initialisation steps to run before the worker can start
            processing jobs

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        """
        raise NotImplementedError()

    @abc.abstractproperty
    def _job_queue(self) -> mp.Queue:
        """
        Defines the shared queue from which the worker will receive work.

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        :return: Queue to receive work from.
        :rtype: mp.Queue
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _is_work_complete(self) -> bool:
        """
        Logic to determine when all of the samples have been processed by
            the pool of workers

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        :return: True if all jobs to be done are completed, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError()

    @property
    def is_ready(self) -> bool:
        """
        Returns True if a worker is ready to receive work, otherwise False.

        :return: True if a worker is ready to receive work, otherwise False.
        :rtype: bool
        """
        return self._shared_state.is_ready.value

    @property
    def is_done(self) -> bool:
        """
        Returns True is a worker has completed all its work, otherwise False.

        :return: True is a worker has completed all its work, otherwise False.
        :rtype: bool
        """
        return self._shared_state.is_done.value

    @property
    def is_ray_casting_done(self) -> bool:
        """
        Returns True if all the ray casting work has been completed,
            otherwise False.

        :return: True if all the ray casting work has been completed,
            otherwise False.
        :rtype: bool
        """
        return self._shared_state.is_ray_casting_done.value

    @property
    def n_complete(self) -> int:
        """
        Returns the global number of completed tasks.

        :return: The global number of completed tasks.
        :rtype: int
        """
        return self._shared_state.n_complete.value

    @property
    def ray_cast_queue(self) -> mp.Queue:
        """
        Returns the shared multiprocessing Queue used for ray casting tasks.

        :return: The multiprocessing Queue used for ray casting tasks.
        :rtype: mp.Queue
        """
        return self._shared_state.ray_cast_queue

    @property
    def generation_queue(self) -> mp.Queue:
        """
        Returns the shared multiprocessing Queue used for data generation tasks.


        :return: The multiprocessing Queue used for data generation tasks.
        :rtype: mp.Queue
        """
        return self._shared_state.generation_queue

    @property
    def track_mesh_path(self) -> Path:
        """
        Returns a Path to the track mesh file.

        :return: The Path to the track mesh file.
        :rtype: Path
        """
        return Path(self._config["track_mesh_path"])

    @property
    def modified_mesh_path(self) -> Path:
        """Returns a Path to the modified track mesh file.

        :return: The Path to the modified track mesh file.
        :rtype: Path
        """
        return self.track_mesh_path.parent / "tmp.obj"

    @property
    def recording_path(self) -> Path:
        """Returns a Path to the folder containing recorded data.

        :return: The Path to the folder containing recorded data.
        :rtype: Path
        """
        return Path(self._config["recorded_data_path"])

    @property
    def output_path(self) -> Path:
        """
        Returns a Path to the folder where generated data should be written.

        :return: The Path to the folder where generated data should be written.
        :rtype: Path
        """
        return Path(self._config["output_path"])

    @property
    def image_size(self) -> List[int]:
        """
        Returns a list of integers representing the image's width and height in
            pixels.

        :return: A list of integers representing the image's width and height
            in pixels.
        :rtype: List[int]
        """
        return self._config["image_size"]

    @property
    def track_name(self) -> str:
        """
        Returns the name of the track.

        :return: The name of the track.
        :rtype: str
        """
        return self._config["track_name"]

    @property
    def car_name(self) -> str:
        """
        Returns the name of the car.

        :return: The name of the car.
        :rtype: str
        """
        return self._config["car_name"]

    def increment_n_complete(self):
        """
        Increments the number of globally completed tasks.
        """
        with self._shared_state.n_complete.get_lock():
            self._shared_state.n_complete.value += 1

    def set_as_ready(self):
        """
        Sets the worker as ready to receive work.
        """
        self._shared_state.is_ready.value = True

    def set_as_done(self):
        """
        Sets the worker having finished all the available work .
        """
        self._shared_state.is_done.value = True

    def _setup_scene(self):
        """
        Loads a modified track mesh.
        """
        self._scene = load_track_mesh(
            self.track_mesh_path,
            self.modified_mesh_path,
            self.track_name,
        )
