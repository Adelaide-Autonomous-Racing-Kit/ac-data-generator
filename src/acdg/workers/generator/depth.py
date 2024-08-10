import numpy as np
from acdg.workers.generator.base import DataGenerator
from acdg.workers.generator.utils import (
    allocate_empty_frame,
    convert_to_uint8,
    noramlise_values,
    reverse_sign_of_values,
)
import trimesh


class DepthMapGenerator(DataGenerator):
    def generate(self):
        """
        Calls all methods registered in configuration to generate depth data.
        """
        [method() for method in self._generation_methods]

    def _generate_visualised_depth_map(self):
        """
        Generates a visualised depth map and saves it.
        """
        depth_map = self._get_depth_map()
        self._save_depth_map(depth_map)

    def _get_depth_map(self) -> np.array:
        """
        Returns a depth map for the sample.

        :returns: Depth map
        :rtype: np.array
        """
        depth = self._calculate_depth()
        self._visualise_depth_map(depth)
        depth_map = allocate_empty_frame(*self._image_size)
        self._insert_values_into_image(depth, depth_map)
        return depth_map

    def _calculate_depth(self) -> np.array:
        """
        Returns the depth at each pixel location.

        :return: Depth map.
        :rtype: np.array
        """
        return calculate_depth(self._hit_to_camera, self._ray_directions)

    def _visualise_depth_map(self, depth: np.array):
        """
        Converts the raw depth measurement into normalised uint8 values between
            0 and 255 for visualisation.

        :param depth_map: A raw depth map.
        :type depth_map: np.array
        """
        noramlise_values(depth)
        reverse_sign_of_values(depth)
        convert_to_uint8(depth)

    def _save_depth_map(self, depth_map: np.array):
        """
        Save visualised depth map.

        :param depth_map: A visualised depth map.
        :type depth_map: np.array
        """
        self._save_data(f"{self._record_number}-depth.png", depth_map)

    def _setup(self):
        """
        Specific setup steps for DepthMapGenerator.
        """
        self._register_generation_methods()

    def _register_generation_methods(self):
        """
        Registers data generation methods to call based on user configuration.
        """
        generator_config = self._worker._config["generate"]["depth"]
        if "visuals" in generator_config:
            method = self._generate_visualised_depth_map
            self._generation_methods.append(method)
        if "data" in generator_config:
            raise NotImplementedError()


def calculate_depth(hit_to_camera: np.array, directions: np.array) -> np.array:
    """
    Calculates the depth from image plane pixel to ray collision.

    :param hit_to_camera: Vectors from camera origin to ray collision location.
    :type hit_to_camera: np.array
    :param directions: Unit vectors in the direction of the camera pixel rays.
    :type directions: np.array
    :return: Distances from image plane pixels to collision location
    :rtype: np.array
    """
    return trimesh.util.diagonal_dot(hit_to_camera, directions)
