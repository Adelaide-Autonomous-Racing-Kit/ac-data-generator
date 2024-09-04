from acdg.tracks import TRACK_DATA
from acdg.tracks.constants import COLOUR_LIST, TRAIN_ID_LIST
from acdg.utils.load import load_image
from acdg.workers.generator.base import DataGenerator
from acdg.workers.generator.utils import allocate_empty_frame, rgb_to_bgr
import cv2
import numpy as np
import trimesh


class SegmentationGenerator(DataGenerator):
    def generate(self):
        """
        Calls all methods registered in configuration to generate normal data.
        """
        pixel_ids = self._get_semantic_pixel_ids()
        for method in self._generation_methods:
            method(pixel_ids)

    def _get_semantic_pixel_ids(self) -> np.array:
        """
        Returns a semantic id for each pixel in the image.

        :return: A semantic id map of the image.
        :rtype: np.array
        """
        i_tri = np.copy(self._i_triangles)
        i_tri[i_tri != -1] = self._triangle_to_id[i_tri[i_tri != -1]]
        if self._is_generating_depth:
            pixel_ids = -1 * (allocate_empty_frame(*self._image_size) + 1)
            self._insert_values_into_image(i_tri, pixel_ids)
        else:
            pixel_ids = i_tri.reshape(self._image_size)
        return pixel_ids

    def _generate_visualised_semantics(self, pixel_ids: np.array):
        """
        Generates a visualised semantic map of the image and saves it.

        :param pixel_ids: A semantic id map.
        :type pixel_ids: np.array
        """
        visualised_map = get_visualised_semantics(pixel_ids)
        self._save_colour_map(visualised_map)

    def _save_colour_map(self, colour_map: np.array):
        """
        Save the visualised semantic map.

        :param colour_map: A visualised semantic map
        :type colour_map: np.array
        """
        self._save_data(f"{self._record_number}-seg_colour.png", colour_map)

    def _generate_semantic_training_data(self, pixel_ids: np.array):
        """
        Generates semantic segmentation training data and saves it.

        :param pixel_ids: A semantic id map.
        :type pixel_ids: np.array
        """
        id_map = get_semantic_training_data(pixel_ids)
        self._save_segmentation_map(id_map)

    def _save_segmentation_map(self, ids_map: np.array):
        """
        Save semantic segmentation training data.

        :param ids_map: Semantic segmentation training data
        :type ids_map: np.array
        """
        self._save_data(f"{self._record_number}-trainids.png", ids_map)

    def _generate_overlaid_visualisation(self, pixel_ids: np.array):
        """
        Overlays the visualised semantic map ontop of the captured frame and
            saves it.

        :param pixel_ids: A semantic id map.
        :type pixel_ids: np.array
        """
        image = load_image(self._captured_frame_path)
        overlaid = get_overlaid_segmentation_visualisation(
            pixel_ids,
            image,
            not self._is_generating_depth,
        )
        self._save_overlaid_visualisation(overlaid)

    def _save_overlaid_visualisation(self, overlaid: np.array):
        """
        Save semantic colour map overlaid onto game frame.

        :param overlaid: Overlaid visualisation
        :type overlaid: np.array
        """
        self._save_data(f"{self._record_number}-seg_overlay.png", overlaid)

    def _setup(self):
        """
        Specific setup steps for SegmentationGenerator.
        """
        self._setup_triangle_to_id_map()
        self._register_generation_methods()

    def _setup_triangle_to_id_map(self):
        """
        Creates a mapping between triangle indexes and their semantic class
        """
        scene, track_name = self._worker._scene, self._worker.track_name
        triangle_to_id = get_triangle_to_semantic_id_map(scene, track_name)
        self._triangle_to_id = triangle_to_id

    def _register_generation_methods(self):
        """
        Registers data generation methods to call based on user configuration.
        """
        generator_config = self._worker._config["generate"]["segmentation"]
        if "visuals" in generator_config:
            method = self._generate_visualised_semantics
            self._generation_methods.append(method)
        if "data" in generator_config:
            method = self._generate_semantic_training_data
            self._generation_methods.append(method)
        if "overlays" in generator_config:
            method = self._generate_overlaid_visualisation
            self._generation_methods.append(method)


def get_triangle_to_semantic_id_map(
    scene: trimesh.Scene,
    track_name: str,
) -> np.array:
    """
    Returns a mapping between triangle indexes and the semantic ID of
        that triangle's geometry.

    :param scene: The trimesh.Scene object for the track
    :type scene: trimesh.Scene
    :return: Triangle index to semantic class id map
    :rtype: np.array
    """
    triangle_to_node = scene.triangles_node
    material_to_id = TRACK_DATA[track_name].material_to_id
    triangle_to_id = [material_to_id[name] for name in triangle_to_node]
    return np.asarray(triangle_to_id, dtype=np.uint8)


def get_semantic_training_data(pixel_ids: np.array) -> np.array:
    """
    Maps pixel ids to semantic ids, returning semantic segmentation training
        data.

    :param pixel_ids: A semantic id map.
    :type pixel_ids: np.array
    :return: Semantic segmentation training data
    :rtype: np.array
    """
    id_map = np.array(TRAIN_ID_LIST[pixel_ids], dtype=np.uint8)
    return id_map


def get_visualised_semantics(pixel_ids: np.array) -> np.array:
    """
    Maps pixel ids to a colour specific to semantic classes for visualisation.

    :param pixel_ids: A semantic id map.
    :type pixel_ids: np.array
    :return: Visualised segmentation map
    :rtype: np.array
    """
    visualised_map = np.array(COLOUR_LIST[pixel_ids], dtype=np.uint8)
    visualised_map = rgb_to_bgr(visualised_map)
    return visualised_map


def get_overlaid_segmentation_visualisation(
    pixel_ids: np.array,
    image: np.array,
    flipud: bool,
) -> np.array:
    """
    Overlays the visualised semantic segmentation map onto the corresponding
        game frame.

    :param pixel_ids: A semantic id map.
    :type pixel_ids: np.array
    :param image: Game frame to be overlaid.
    :type image: np.array
    :param flipud: Whether to flip the image along the horizontal axis.
    :type flipud: bool
    :return: Overlaid combination of colour map and frame
    :rtype: np.array
    """
    visualised_semantics = get_visualised_semantics(pixel_ids)
    image = np.rot90(image, axes=(1, 0))
    if flipud:
        image = np.flipud(image)
    return cv2.addWeighted(image, 0.5, visualised_semantics, 0.5, 0.0)
