#!/usr/bin/env python
# -*- coding: utf-8
# Functions that perform mathematical operations on an image.


import logging
import numpy as np

from skimage.morphology import erosion, dilation, disk, ball, square, cube


logger = logging.getLogger(__name__)


def _get_selem(shape, size, dim):
    """
    Create structuring element of desired shape and radius
    :param shape: str: Shape of the structuring element. See available options below in the code
    :param size: int: size of the element.
    :param dim: {0, 1, 2}: Dimension of the array which 2D structural element will be orthogonal to. For example, if
    you wish to apply a 2D disk kernel in the X-Y plane, leaving Z unaffected, parameters will be: shape=disk, dim=2.
    :return: numpy array: structuring element
    """
    # TODO: enable custom selem
    if shape == 'square':
        selem = square(size)
    elif shape == 'cube':
        selem = cube(size)
    elif shape == 'disk':
        selem = disk(size)
    elif shape == 'ball':
        selem = ball(size)
    else:
        ValueError("This shape is not a valid entry: {}".format(shape))

    if not (len(selem.shape) in [2, 3] and selem.shape[0] == selem.shape[1]):
        raise ValueError("Invalid shape")

    # If 2d kernel, replicate it along the specified dimension
    if len(selem.shape) == 2:
        selem3d = np.zeros([selem.shape[0]]*3)
        imid = np.floor(selem.shape[0] / 2).astype(int)
        if dim == 0:
            selem3d[imid, :, :] = selem
        elif dim == 1:
            selem3d[:, imid, :] = selem
        elif dim == 2:
            selem3d[:, :, imid] = selem
        else:
            raise ValueError("dim can only take values: {0, 1, 2}")
        selem = selem3d
    return selem


def dilate(data, size, shape, dim=None):
    """
    Dilate data using ball structuring element
    :param data: numpy array: 2d or 3d array
    :param size: int: If shape={'square', 'cube'}: Corresponds to the length of an edge (size=1 has no effect).
    If shape={'disk', 'ball'}: Corresponds to the radius, not including the center element (size=0 has no effect).
    :param shape: {'square', 'cube', 'disk', 'ball'}
    :param dim: {0, 1, 2}: Dimension of the array which 2D structural element will be orthogonal to. For example, if
    you wish to apply a 2D disk kernel in the X-Y plane, leaving Z unaffected, parameters will be: shape=disk, dim=2.
    :return: numpy array: data dilated
    """
    return dilation(data, selem=_get_selem(shape, size, dim), out=None)


def erode(data, size, shape, dim=None):
    """
    Dilate data using ball structuring element
    :param data: numpy array: 2d or 3d array
    :param size: int: If shape={'square', 'cube'}: Corresponds to the length of an edge (size=1 has no effect).
    If shape={'disk', 'ball'}: Corresponds to the radius, not including the center element (size=0 has no effect).
    :param shape: {'square', 'cube', 'disk', 'ball'}
    :param dim: {0, 1, 2}: Dimension of the array which 2D structural element will be orthogonal to. For example, if
    you wish to apply a 2D disk kernel in the X-Y plane, leaving Z unaffected, parameters will be: shape=disk, dim=2.
    :return: numpy array: data dilated
    """
    return erosion(data, selem=_get_selem(shape, size, dim), out=None)
