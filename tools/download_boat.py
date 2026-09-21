"""Download the 512 x 512 greyscale ``Fishing Boat`` test image.

The image is retrieved from the USC-SIPI database and saved to both
``lab2/img/boat.png`` and ``lab4/img/boat.png``.

Source: https://sipi.usc.edu/database/database.php?volume=misc
(``Miscellaneous`` volume, file ``boat.512``)

Run from any directory with::

    python tools/download_boat.py
"""

import io
import os
import urllib.request
import zipfile

import numpy as np
from PIL import Image

URL = "https://sipi.usc.edu/database/misc.zip"  # complete volume archive (~12 MB)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

print("Downloading", URL, "...")
with urllib.request.urlopen(URL) as response:
    data = response.read()

with zipfile.ZipFile(io.BytesIO(data)) as archive:
    # Locate boat.512 regardless of its directory inside the archive.
    names = [n for n in archive.namelist() if "boat.512" in n.lower()]
    if not names:
        raise FileNotFoundError("boat.512 was not found in misc.zip")
    with archive.open(names[0]) as f:
        img = Image.open(io.BytesIO(f.read())).convert("L")

arr = np.array(img)
for lab in ("lab2", "lab4"):
    path = os.path.join(root, lab, "img", "boat.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print("saved:", os.path.join(lab, "img", "boat.png"))
print("shape", arr.shape, "values in [%d, %d] (expected for the original: [0, 239])" % (arr.min(), arr.max()))
