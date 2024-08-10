from pathlib import Path

import cv2
import numpy as np


def rgb_to_bgr(image: np.array) -> np.array:
    """
    Convert an RGB image to a BGR image.

    :param image: An image to convert.
    :type image: np.array
    :return: Converted image.
    :rtype: np.array
    """
    return image[:, :, ::-1]


def noramlise_values(values: np.array) -> np.array:
    """
    Normalise an array of values inplace to have values between 0.0 and 1.0.

    :param values: The array to normalise.
    :type values: np.array
    """
    values -= values.min()
    values /= values.ptp()


def reverse_sign_of_values(values: np.array):
    """
    Reverse the sign of an array of  normalised values inplace.

    :param values: An array containing values to reverse the sign of.
    :type values: np.array
    """
    values -= 1
    values *= -1


def convert_to_uint8(values: np.array) -> np.array:
    """
    Inplace conversion of an array of normalised floating-point values to
        unsigned 8-bit integers.
    """
    values *= 255
    values.astype(np.uint8, copy=False)


def allocate_empty_frame(
    width: int,
    height: int,
    channels: int = 0,
) -> np.array:
    """
    Allocate an frame of zeros of specified width, height, and number of
        channels.

    :param width: Width of the frame to allocate in pixels.
    :type width: int
    :param height: Height of the frame to allocate in pixels.
    :type height: int
    :param channels: Number of channels to allocate.
    :type channels: int
    :return: Allocated frame filled with zeros.
    :rtype: np.array
    """
    shape = (width, height)
    if channels > 0:
        shape = (*shape, channels)
    return np.zeros(shape, dtype=np.uint8)


def save_image(to_save: np.array, filepath: Path, flipud: bool):
    """
    Rotate and save an image to file.

    :param to_save: Image to rotate and save.
    :type to_save: np.array
    :param filepath: Filepath of where to save the image to.
    :type filepath: Path
    :param flipud: Whether to flip the image along the horizontal axis before
        saving.
    :type flipud: bool
    """
    to_save = np.rot90(to_save)
    if flipud:
        to_save = np.flipud(to_save)
    cv2.imwrite(str(filepath), to_save)
