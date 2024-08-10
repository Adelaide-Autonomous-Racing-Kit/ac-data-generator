from acdg.workers.generator.base import DataGenerator
from acdg.workers.generator.utils import (
    allocate_empty_frame,
    convert_to_uint8,
    noramlise_values,
)
import numpy as np
import trimesh


class NormalMapGenerator(DataGenerator):
    def generate(self):
        """
        Calls all methods registered in configuration to generate normal data.
        """
        [method() for method in self._generation_methods]

    def _generate_visualised_normal_map(self):
        """
        Generates a visualised normal map and saves it.
        """
        normal_map = self._get_normal_map()
        self._save_normal_map(normal_map)

    def _get_normal_map(self):
        """
        Generates a visualised normal map.

        :return: A visualised normal map.
        :rtype: np.array
        """
        normals = self._triangle_to_normal[self._i_triangles]
        self._visualise_normal_map(normals)
        if self._is_generating_depth:
            shape = self._image_size
            normal_map = allocate_empty_frame(*shape, channels=3)
            self._insert_values_into_image(normals, normal_map)
        else:
            normal_map = normals.reshape((*self._image_size, 3))
        return normal_map

    def _visualise_normal_map(self, normals: np.array):
        """
        Converts the raw normal vectors into normalised uint8 values between 0
            and 255 for visualisation.

        :param normals: A raw normal map.
        :type normals: np.array
        """
        noramlise_values(normals)
        convert_to_uint8(normals)

    def _save_normal_map(self, normal_map: np.array):
        """
        Save visualised normal map.

        :param normal_map: A visualised normal map.
        :type normal_map: np.array
        """
        self._save_data(f"{self._record_number}-normals.png", normal_map)

    def _setup(self):
        """
        Specific setup steps for NormalMapGenerator.
        """
        self._setup_triangle_to_normal_map()
        self._register_generation_methods()

    def _setup_triangle_to_normal_map(self):
        """
        Creates a mapping between triangle indexes and their respective surface
            normal vector.
        """
        triangle_to_normal = get_triangle_to_normal_map(self._worker._scene)
        self._triangle_to_normal = triangle_to_normal

    def _register_generation_methods(self):
        """
        Registers data generation methods to call based on user configuration.
        """
        generator_config = self._worker._config["generate"]["normals"]
        if "visuals" in generator_config:
            method = self._generate_visualised_normal_map
            self._generation_methods.append(method)
        if "data" in generator_config:
            raise NotImplementedError()


def get_triangle_to_normal_map(scene: trimesh.Scene) -> np.array:
    """
    Returns a mapping between triangle indexes and surface normal vectors of
        a triangle's face.

    :param scene: The trimesh.Scene object for the track
    :type scene: trimesh.Scene
    :return: Triangle index to surface normal vector map
    :rtype: np.array
    """
    normals, valid = trimesh.triangles.normals(scene.triangles)
    triangle_to_normal = np.zeros((valid.shape[0], 3), dtype=np.float32)
    triangle_to_normal[valid] = normals
    return triangle_to_normal
