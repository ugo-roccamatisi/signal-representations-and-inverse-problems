"""Audio-file loader used by Lab 3."""

import numpy as np
from scipy.io.wavfile import read

__all__ = ["load_sound"]


def load_sound(file, n0, s=0):
    """Load ``n0`` samples from a WAV file and return a one-dimensional array.

    file : path to the WAV file
    n0   : requested number of samples, starting at index ``s``
    s    : index of the first retained sample (zero by default)

    For stereo input, retain only the first channel. If the file is shorter
    than ``s + n0``, pad it with zeros so that the returned vector always has
    exactly ``n0`` samples; the notebook assigns it to a fixed-size row.
    """
    fs, x = read(file)
    if x.ndim > 1:
        x = x[:, 0]  # first channel
    x = x.astype(float)
    x = x[s:s + n0]
    if x.size < n0:
        x = np.concatenate([x, np.zeros(n0 - x.size)])
    return x
