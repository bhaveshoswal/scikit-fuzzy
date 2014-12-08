"""
imops.py : scikit-fuzzy subpackage for 2-D fuzzy processing, usually applied
           to image data.

"""

import numpy as np
from .arraypad import pad
from .shape import view_as_windows


def defocus_local_means(I):
    """
    Defocusing non-normalized image I using local arithmatic mean.

    Parameters
    ----------
    I : ndarray
        Input image; normalization not required.

    Returns
    -------
    D : ndarray of floats, same shape as I
        Defocused output image. By definition will not extend the range of `I`
        but the result will be an array of floats.

    Notes
    -----
    Reduces 'salt & pepper' noise in a quantized image by taking the
    arithmatic mean of the 4-connected neighborhood. So the new value at X

            +---+
            | c |
        +---+---+---+
        | a | X | b |
        +---+---+---+
            | d |
            +---+

    is defined by

        X = 0.25 * (a + b + c + d)

    """
    # Pad input
    J = pad(I.astype(np.float64), ((1, 1), (1, 1)), mode='reflect')

    # Rolling windows into array
    J = view_as_windows(J, (3, 3))

    # Slice out & average along axis representing 4 nearest neighbors
    return J[:, :, [1, 1, 0, 2], [0, 2, 1, 1]].mean(axis=2)
