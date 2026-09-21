"""Replacement module used by RSP Labs 1 and 2.

The original Moodle module is unavailable. This file provides the names that
the notebooks use without importing them explicitly:

- pylab-style plotting functions: figure, plot, grid, xlabel, ylabel, title,
  subplot, legend, colorbar, pcolormesh, show, and tight_layout;
- NumPy helpers: arange, linspace, and randn;
- the Hann window, removed from scipy.signal in recent SciPy versions;
- Bokeh and ipywidgets helpers for the interactive Lab 1 visualisation;
- the psnr and plot_wavelet helpers used in Lab 2.
"""

import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# Pylab-style plotting helpers
# --------------------------------------------------------------------------
from matplotlib.pyplot import (
    figure, plot, grid, xlabel, ylabel, title, subplot, legend,
    colorbar, pcolormesh, show, tight_layout, imshow, axis, xlim, ylim,
)

# --------------------------------------------------------------------------
# numpy
# --------------------------------------------------------------------------
from numpy import arange, linspace, pi, exp, sqrt, log10, zeros, ones
from numpy.random import randn

# --------------------------------------------------------------------------
# Hann window (scipy.signal.hann was removed in SciPy 1.13)
# --------------------------------------------------------------------------
try:
    from scipy.signal.windows import hann
except ImportError:  # compatibility with older SciPy versions
    from scipy.signal import hann

# --------------------------------------------------------------------------
# Bokeh / ipywidgets (interactive Lab 1 visualisation)
# --------------------------------------------------------------------------
try:
    from bokeh.plotting import figure as _bk_figure
    from bokeh.plotting import show as bkshow
    from bokeh.io import push_notebook, output_notebook

    def bkfigure(*args, **kwargs):
        """Wrapper de bokeh.plotting.figure.

        Bokeh >= 3 renamed plot_width/plot_height to width/height. Translate
        the legacy names so the notebook works with either API.
        """
        if "plot_width" in kwargs:
            kwargs["width"] = kwargs.pop("plot_width")
        if "plot_height" in kwargs:
            kwargs["height"] = kwargs.pop("plot_height")
        return _bk_figure(*args, **kwargs)

    try:
        output_notebook(hide_banner=True)  # render Bokeh figures in Jupyter
    except Exception:
        pass
except ImportError:
    def _missing(*args, **kwargs):
        raise ImportError("Bokeh is not installed: pip install bokeh")
    bkfigure = bkshow = push_notebook = output_notebook = _missing

try:
    from ipywidgets import interact
except ImportError:
    def interact(*args, **kwargs):
        raise ImportError("ipywidgets is not installed: pip install ipywidgets")


# --------------------------------------------------------------------------
# Lab 2 : PSNR
# --------------------------------------------------------------------------
def psnr(x, y, vmax=-1):
    """Peak signal-to-noise ratio in dB between images x and y.

    PSNR = 10 log10(vmax^2 / MSE). If vmax < 0, use the largest absolute
    value found in either x or y.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if vmax < 0:
        vmax = max(np.abs(x).max(), np.abs(y).max())
    mse = np.mean((x - y) ** 2)
    if mse == 0:
        return np.inf
    return 10 * np.log10(vmax ** 2 / mse)


# --------------------------------------------------------------------------
# Lab 2: display a 2D wavelet transform
# --------------------------------------------------------------------------
def _rescale(a):
    """Linearly rescale an array to [0, 1]."""
    a = np.asarray(a, dtype=float)
    lo, hi = a.min(), a.max()
    return (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)


def _rescale_wav(a):
    """Symmetrically rescale detail coefficients so zero maps to mid-grey."""
    v = np.abs(a).max()
    return 0.5 + 0.5 * a / v if v > 0 else 0.5 * np.ones_like(a)


def plot_wavelet(fW, Jmin=0):
    """Display the coefficients of a 2D wavelet transform.

    fW   : square n x n array (n is a power of two) returned by
           pywt.coeffs_to_array in ``periodization`` mode.
    Jmin : coarsest scale, equal to log2(n) - J for J levels.

    The approximation appears in the upper-left corner. Each detail block is
    rescaled independently, and red lines separate the scales.
    """
    fW = np.asarray(fW, dtype=float)
    n = fW.shape[1]
    Jmax = int(np.log2(n)) - 1
    U = fW.copy()
    for j in range(Jmax, Jmin - 1, -1):
        a, b = 2 ** j, 2 ** (j + 1)
        U[:a, a:b] = _rescale_wav(U[:a, a:b])
        U[a:b, :a] = _rescale_wav(U[a:b, :a])
        U[a:b, a:b] = _rescale_wav(U[a:b, a:b])
    c = 2 ** Jmin
    U[:c, :c] = _rescale(U[:c, :c])

    plt.imshow(U, cmap="gray", interpolation="nearest", vmin=0, vmax=1)
    for j in range(Jmax, Jmin - 1, -1):
        a, b = 2 ** j, 2 ** (j + 1)
        plt.plot([0, b - 1], [a, a], "r", linewidth=1)
        plt.plot([a, a], [0, b - 1], "r", linewidth=1)
    plt.xlim(0, n - 1)
    plt.ylim(n - 1, 0)
    plt.axis("off")
