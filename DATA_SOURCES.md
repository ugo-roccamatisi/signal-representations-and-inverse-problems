# Data and resource provenance

This document distinguishes course resources, standard test images, and generated substitutes used when the original files were unavailable.

| File | Status |
| --- | --- |
| `lab1/sounds/bird.wav` | Course recording, short version: 16,384 samples at 15 kHz |
| `lab1/sounds/glockenspiel_mono.wav` | Synthetic substitute |
| `lab1/sounds/desactive_mono.wav` | Synthetic substitute |
| `lab1/signal_2sinus.mat` | Synthetic substitute |
| `lab2/img/chessboard.png` | Locally generated 512 × 512 chessboard |
| `lab2/img/boat.png` and `lab4/img/boat.png` | “Boat” test image from the USC-SIPI database |
| `lab2/img/lena.jpg` | “Lena” test image |
| `lab3/nt_toolbox/data/*.wav` | Audio recordings used in the course |
| `module_TDS.py`, `plotwavelet.py`, `nt_toolbox/` | Replacements for unavailable Moodle modules |

## Regenerating the substitute resources

Run the following commands from the repository root:

```bash
python tools/generate_substitute_sounds.py
python tools/generate_substitute_images.py
python tools/download_boat.py
```

The `download_boat.py` script requires network access.

## Public distribution

Before publishing this repository, verify that the distribution terms of the course resources, the USC-SIPI database, and the “Lena” image permit redistribution. If they do not, remove the affected files and document how users can obtain them independently.
