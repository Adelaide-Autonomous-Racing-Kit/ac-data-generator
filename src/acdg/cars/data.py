from dataclasses import dataclass
from typing import List


@dataclass
class CarData:
    """
    Stores data related to the camera of a car, including its position and pitch.

    :param camera_offset_x: Camera offset in the x direction.
    :type camera_offset_x: float
    :param camera_offset_y: Camera offset in the y direction.
    :type camera_offset_y: float
    :param camera_offset_z: Camera offset in the z direction.
    :type camera_offset_z: float
    :param camera_pitch: Pitch offset applied to the car's camera.
    :type camera_pitch: float
    """

    camera_offset_x: float
    camera_offset_y: float
    camera_offset_z: float
    camera_pitch: float

    @property
    def camera_offset_xyz(self) -> List[float]:
        """
        A list containing the x, y, and z offsets of the camera in car coordinates.

        :return: The x, y, and z offsets of the camera in car coordinates.
        :rtype: List[int]
        """
        return [self.camera_offset_x, self.camera_offset_y, self.camera_offset_z]
