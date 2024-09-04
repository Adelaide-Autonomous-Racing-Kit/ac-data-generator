from dataclasses import dataclass
from typing import Dict, List

from acdg.tracks.constants import SEMANTIC_NAME_TO_ID


@dataclass
class TrackData:
    """
    A data class to store track specific data.

    :param geometries_to_remove: A list of geometries to remove.
    :type geometries_to_remove: List[str]
    :param vertex_groups_to_modify: A list of vertex groups to modify.
    :type vertex_groups_to_modify: List[str]
    :param material_to_semantics: A dictionary mapping material names to
        semantic names.
    :type material_to_semantics: Dict[str, str]
    """

    geometries_to_remove: List[str]
    vertex_groups_to_modify: List[str]
    material_to_semantics: Dict[str, str]

    def __post_init__(self):
        """
        Creates a mapping between material names and semantic ids
        """
        self.material_to_id = {
            material: SEMANTIC_NAME_TO_ID[semantic_name]
            for material, semantic_name in self.material_to_semantics.items()
        }
