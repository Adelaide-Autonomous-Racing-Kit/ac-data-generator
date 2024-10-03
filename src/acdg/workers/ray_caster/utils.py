import math
from typing import Dict, List

from acdg.cars import CAR_DATA
from scipy.spatial.transform import Rotation
import trimesh

# Set trimesh's rotation order to extrinsic xyz
trimesh.transformations.euler_matrix.__defaults__ = ("sxyz",)


def calculate_horizontal_fov(
    vertical_fov: float,
    width: int,
    height: int,
) -> float:
    """
    Calculates and returns the camera's horizontal field of view in degrees,
    given the camera's image plane height and width in pixels and vertical
    field of view in degrees.

    :param vertical_fov: Vertical field of view in degrees.
    :type vertical_fov: float
    :param width: Image plane width in pixels.
    :type width: int
    :param height: Image plane height in pixels.
    :type height: int
    :return: Horizontal field of view in degrees.
    :rtype: float
    """
    focal_length = height / math.tan(math.radians(vertical_fov) / 2)
    return math.degrees(2 * math.atan(width / focal_length))


def convert_scene_to_collision_mesh(
    scene: trimesh.Scene,
) -> trimesh.ray.ray_pyembree.RayMeshIntersector:
    """
    Concatenates all the geometry nodes in a scene into a single trimesh.Mesh
        object and instantiates a RayMeshIntersector with it. The triangle
        indexes of the concatenated mesh align with the original scene, so
        collisions returned my the mesh intersector and be used index the scene
        which they are made from.


    :param scene: The trimesh.Scene to convert.
    :type scene: trimesh.Scene
    :return: A RayMeshIntersector instance using the converted mesh.
    :rtype: trimesh.ray.ray_pyembree.RayMeshIntersector
    """
    meshes = [mesh for mesh in scene.geometry.values()]
    mesh = trimesh.util.concatenate(meshes)
    return trimesh.ray.ray_pyembree.RayMeshIntersector(mesh)


def get_camera_rotation(state: Dict, car_name: str) -> List[float]:
    """
    Extracts the camera's rotation from a game capture state dictionary.
        Assetto Corsa uses intrinsic yxz rotations that need to be converted
        to extrinsic xyz for trimesh. Cars defined in the game can contain an
        additional pitch offset applied in the car coordinate frame that is
        accounted for here.

    :param state: The game capture state dictionary.
    :type state: Dict
    :param car_name: The name of the car.
    :type car_name: str
    :return: A list of Euler angles in radians representing the camera's
        extrinsic rotation about the x, y, and z axes in that order.
    :rtype: List[float]
    """
    pitch_offset = CAR_DATA[car_name].camera_pitch
    car_rotation = get_car_rotation(state)
    camera_pitch = Rotation.from_euler("X", pitch_offset, degrees=True)
    camera_rotation = car_rotation * camera_pitch
    extrinsic_euler_angles = camera_rotation.as_euler("xyz", degrees=False)
    return extrinsic_euler_angles.tolist()


def get_camera_location(state: Dict, car_name: str) -> List[float]:
    """
    Extracts the camera's location from a game capture state dictionary. Cars
        in the game provide an additional spatial offset, in the car coordinate
        frame, for the different camera locations defined on the vehicle. An
        additional pi rotation about the y axis is also applied to adjust for
        a -z forward convention used by the world coordinate frame.

    :param state: The game capture state dictionary.
    :type state: Dict
    :param car_name: The name of the car.
    :type car_name: str
    :return: A list representing the camera's location in [X, Y, Z].
    :rtype: List[float]
    """
    camera_offset = CAR_DATA[car_name].camera_offset_xyz
    car_rotation = get_car_rotation(state)
    z_flip = Rotation.from_euler("Y", math.pi, degrees=False)

    # camera_offset[2] = -camera_offset[2]
    camera_offset = (car_rotation * z_flip).apply(camera_offset)
    location = [
        state["ego_location_x"] + camera_offset[0],
        state["ego_location_y"] + camera_offset[1],
        state["ego_location_z"] + camera_offset[2],
    ]
    return location


def get_car_rotation(state: Dict) -> Rotation:
    """
    Returns a scipy.spatial.transform.Rotation object representing the rotation
        of the car in the given game state dictionary. The world coordinate
        frame uses a -z forward convention that is accounted for by adding an
        additional pi radians to the captured heading.

    :param state: The game capture state dictionary.
    :type state: Dict
    :return: A scipy.spatial.transform.Rotation object representing the car's
        rotation.
    :rtype: scipy.spatial.transform.Rotation
    """
    r_x = Rotation.from_euler("X", state["pitch"], degrees=False)
    r_y = Rotation.from_euler("Y", -state["heading"] + math.pi, degrees=False)
    r_z = Rotation.from_euler("Z", state["roll"], degrees=False)
    return r_y * r_x * r_z
