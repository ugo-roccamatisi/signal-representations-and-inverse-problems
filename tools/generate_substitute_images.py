"""Generate the substitute chessboard image used in Lab 2.

The output is a 512 x 512 chessboard with 8 x 8 squares, each 64 pixels wide.
Square boundaries lie on multiples of 2^6, preserving the Haar-wavelet
property studied in Lab 2, Exercise 2.

This script does not modify the ``boat`` or ``lena`` test images. Use
``download_boat.py`` to retrieve the boat image again.

Run from any directory with::

    python tools/generate_substitute_images.py
"""

import os
import numpy as np
from PIL import Image

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

n, square = 512, 64
i, j = np.indices((n, n))
chessboard = (((i // square) + (j // square)) % 2 * 255).astype(np.uint8)

path = os.path.join(root, "lab2", "img", "chessboard.png")
os.makedirs(os.path.dirname(path), exist_ok=True)
Image.fromarray(chessboard).save(path)
print("created:", os.path.relpath(path, root))
