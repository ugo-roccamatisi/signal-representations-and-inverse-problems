"""Compatibility wrapper used by Lab 2 (``from lib.plotwavelet import *``).

The :func:`plot_wavelet` helper is defined in ``module_TDS.py`` in the same
directory.
"""
try:
    from .module_TDS import plot_wavelet   # package import from lib/
except ImportError:
    from module_TDS import plot_wavelet    # direct import
