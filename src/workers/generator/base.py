import abc
from pathlib import Path
from typing import Dict, List

import numpy as np
from src.workers.generator.utils import save_image


class DataGenerator:
    """
    Base class for deriving classes responsible for turning ray casting results
        into data.

    :param worker_reference: A reference to the worker that will be used for generating data.
    :type worker_reference: Any

    :ivar _worker: A reference to the worker that will be used for generating data.
    :vartype _worker: Any
    :ivar _generation_methods: A list of functions that will be used to generate the data.
    :vartype _generation_methods: List[Callable]
    """

    def __init__(self, worker_reference):
        self._worker = worker_reference
        self._generation_methods = []
        self._setup()

    @abc.abstractmethod
    def generate(self):
        """
        Implement data generation work specific to the data being created

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _setup(self):
        """
        Implement data generator specific setup steps

        :raises NotImplementedError: This method needs to be implemented by the derived class.
        """
        raise NotImplementedError()

    def _save_data(self, filename: str, to_save: np.array):
        """
        Saves the generated data to a file.

        :param filename: The name of the file to save the data as.
        :type filename: str
        :param to_save: The data that will be saved.
        :type to_save: numpy.array
        """
        flip_ud = not self._is_generating_depth
        output_path = self._output_path.joinpath(filename)
        save_image(to_save, output_path, flip_ud)

    def _insert_values_into_image(self, values: np.array, image: np.array):
        """
        Inserts values into an image.

        :param values: The values to be inserted into the image.
        :type values: numpy.array
        :param image: The image where the values will be inserted.
        :type image: numpy.array
        """
        image[self._pixels_to_rays[:, 0], self._pixels_to_rays[:, 1]] = values

    @property
    def _generation_job(self) -> Dict:
        """
        A dictionary containing the current generation job.

        :return: A dictionary containing the current generation job.
        :rtype: dict
        """
        return self._worker._work

    @property
    def _output_path(self) -> Path:
        """
        The output path where the generated data will be saved.

        :return: The output path where the generated data will be saved.
        :rtype: Path
        """
        return Path(self._worker._config["output_path"])

    @property
    def _recording_path(self) -> Path:
        """
        The path to the folder where the recorded data is.

        :return: The path to the folder where the recorded data is.
        :rtype: Path
        """
        return Path(self._worker._config["recorded_data_path"])

    @property
    def _record_number(self) -> str:
        """
        The record number for the current generation job.

        :return: The record number for the current generation job.
        :rtype: str
        """
        return self._worker._work["record_number"]

    @property
    def _captured_frame_path(self) -> Path:
        """
        The path to the current record numbers frame is saved.

        :return: The path to the current record numbers frame is saved.
        :rtype: Path
        """
        return self._recording_path.joinpath(self._record_number + ".jpeg")

    @property
    def _i_triangles(self) -> np.array:
        """
        Triangle indexes for the current generation job.

        :return: Triangle indexes for the current generation job.
        :rtype: numpy.array
        """
        return self._worker._work["i_triangles"]

    @property
    def _pixels_to_rays(self) -> np.array:
        """
        The pixels to rays mapping for the current generation job.

        :return: The pixels to rays mapping for the current generation job.
        :rtype: np.array
        """
        return self._worker._work["pixels_to_rays"]

    @property
    def _hit_to_camera(self) -> np.array:
        """
        Returns a vector from the camera origin to each ray's hit location.

        :return: A vector from the camera origin to each ray's hit location.
        :rtype: np.array
        """
        locations = self._worker._work["locations"]
        origin = self._worker._work["origin"]
        return locations - origin

    @property
    def _ray_directions(self) -> np.array:
        """
        Returns unit vectors in the direction of each of the camera's pixel
            rays.

        :return: unit vectors in the direction of each of the camera's pixel
            rays.
        :rtype: np.array
        """
        directions = self._worker._work["ray_directions"]
        i_ray = self._worker._work["i_rays"]
        return directions[i_ray]

    @property
    def _is_generating_depth(self) -> bool:
        """
        Returns True if depth maps are being generated for the samples.

        :return: True if depth maps are being generated for the samples,
            otherwise False.
        :rtype: bool
        """
        generation_config = self._worker._config["generate"]
        return "depth" in generation_config

    @property
    def _image_size(self) -> List[int]:
        """
        Returns the image size in pixels and width by hight order.

        :return: the image size in pixels and width by hight order.
        :rtype: List[int]
        """

        return self._worker._config["image_size"]
