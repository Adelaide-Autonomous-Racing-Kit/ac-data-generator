from pathlib import Path

import trimesh

from acdg.tracks import TRACK_DATA


def load_track_mesh(
    track_mesh: Path,
    modified_mesh: Path,
    track_name: str,
) -> trimesh.Scene:
    """
    Prepares a collision mesh for generating data from. Modifies and removes
        geometries specified in the track's constants.VERTEX_GROUPS_TO_MODIFY

    :param track_mesh: Path to the track mesh file.
    :type track_mesh: Path
    :param modified_mesh: Path to the modified mesh file.
    :type modified_mesh: Path
    :param track_name: Name of the track.
    :type track_name: str
    :return: A trimesh.Scene object using the modified mesh.
    :rtype: trimesh.Scene
    """
    preprocess_track_mesh(track_mesh, modified_mesh, track_name)
    scene = trimesh.load(modified_mesh)
    scene.delete_geometry(TRACK_DATA[track_name].geometries_to_remove)
    return scene


def preprocess_track_mesh(
    track_mesh: Path,
    modified_mesh: Path,
    track_name: str,
):
    """
    Changes the material of vertex groups specified in VERTEX_GROUPS_TO_MODIFY
        to physics. This material is ignored in the collision mesh used for
        ray casting so it a convenient way to remove vertex groups from the
        mesh.

    :param track_mesh: Path to the track mesh file.
    :type track_mesh: Path
    :param modified_mesh: Path to the modified mesh file.
    :type modified_mesh: Path
    :param track_name: Name of the track.
    :type track_name: str
    """
    is_modifying = False
    source_file = track_mesh.open("r")
    destination_file = modified_mesh.open("w")
    while line := source_file.readline():
        if "g " in line and not "g off" in line:
            is_modifying = False
        if is_vertex_group_to_modify(line, track_name):
            is_modifying = True
        if is_modifying and "usemtl" in line:
            destination_file.write("usemtl physics\n")
        else:
            destination_file.write(line)
    destination_file.close()
    source_file.close()


def is_vertex_group_to_modify(line: str, track_name: str) -> bool:
    """
    Returns True if the line contains any of the vertex group names
        specified in the track specific configuration data

    :param line: Line from the mesh file.
    :type line: str
    :param track_name: Name of the track.
    :type track_name: str
    :return: True if the line contains any of the vertex group names specified
        in the track specific configuration data, False otherwise.
    :rtype: bool
    """
    vertex_groups_to_modify = TRACK_DATA[track_name].vertex_groups_to_modify
    return any([name in line for name in vertex_groups_to_modify])
