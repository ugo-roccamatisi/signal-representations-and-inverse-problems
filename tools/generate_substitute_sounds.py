"""Generate synthetic substitute audio files for Lab 1.

These files replace unavailable course resources from Moodle. They reproduce
comparable signal-processing phenomena but are not the original recordings.

Run from any directory with::

    python tools/generate_substitute_sounds.py

Files are written under ``lab1/`` and replace existing files with the same
names.
"""

import os
import numpy as np
from scipy.io.wavfile import write
from scipy.io import savemat

# Work inside lab1 regardless of the directory from which the script is run.
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lab1"))

rng = np.random.default_rng(0)
os.makedirs("sounds", exist_ok=True)


def to_int16(s):
    """Normalise a signal to [-1, 1] and convert it to 16-bit PCM."""
    s = s / np.max(np.abs(s))
    return (0.9 * s * 32767).astype(np.int16)


# ---------------------------------------------------------------------------
# 1) glockenspiel_mono.wav: sequence of percussive notes with a short attack,
#    exponential decay, and inharmonic partials typical of a metal bar.
# ---------------------------------------------------------------------------
fs = 44100
duration = 4.0
t = np.arange(int(fs * duration)) / fs
notes_hz = [1568, 1760, 1976, 2093, 2349, 2093, 1760, 1568]  # G6 to D7
note_dt = duration / len(notes_hz)
glock = np.zeros_like(t)
for k, f0 in enumerate(notes_hz):
    start = int(k * note_dt * fs)
    tt = t[start:] - t[start]
    for ratio, amp, tau in [(1.0, 1.0, 0.6), (2.76, 0.4, 0.25), (5.40, 0.2, 0.1)]:
        glock[start:] += amp * np.exp(-tt / tau) * np.sin(2 * np.pi * ratio * f0 * tt)
glock += 0.002 * rng.standard_normal(t.size)  # light background noise
write("sounds/glockenspiel_mono.wav", fs, to_int16(glock))

# ---------------------------------------------------------------------------
# 2) desactive_mono.wav: synthetic voice-like signal. A varying ~120 Hz pulse
#    train is shaped by time-varying formants and interrupted by silences.
#    This is not a real voice recording, only a comparable harmonic/formant
#    structure that remains visible on a spectrogram.
# ---------------------------------------------------------------------------
fs = 22050
duration = 2.0
t = np.arange(int(fs * duration)) / fs
f0 = 120 + 25 * np.sin(2 * np.pi * 1.5 * t)  # intonation
phase = 2 * np.pi * np.cumsum(f0) / fs
voice = np.zeros_like(t)
formants = np.array([[700, 1200, 2600], [300, 2300, 3000], [500, 900, 2400]])  # vowels
segment = (t * 3 / duration).astype(int).clip(0, 2)
for h in range(1, 40):  # harmonics of the fundamental frequency
    fh = h * f0
    gain = np.zeros_like(t)
    for j in range(3):
        fj = formants[segment, j]
        gain += np.exp(-((fh - fj) / 120) ** 2) / (j + 1)
    voice += gain * np.sin(h * phase) / h ** 0.3
envelope = (np.sin(np.pi * ((t * 3 / duration) % 1)) ** 0.5)  # syllables
voice *= envelope
voice[(t > 0.62) & (t < 0.72)] = 0  # short silences
voice[(t > 1.30) & (t < 1.38)] = 0
voice += 0.01 * rng.standard_normal(t.size)
write("sounds/desactive_mono.wav", fs, to_int16(voice))

# ---------------------------------------------------------------------------
# 3) signal_2sinus.mat: sum of two nearby sinusoids used in Exercise 5 to
#    determine which window and width separate the frequencies.
#    Variables expected by the notebook: t, x, Fe.
# ---------------------------------------------------------------------------
Fe = 4096
duration = 3.0
t = np.arange(int(Fe * duration)) / Fe
f1, f2 = 440.0, 460.0  # 20 Hz gap: the required frequency resolution must be chosen
x = np.sin(2 * np.pi * f1 * t) + 0.8 * np.sin(2 * np.pi * f2 * t)
x += 0.05 * rng.standard_normal(t.size)
savemat("signal_2sinus.mat", {"t": t[np.newaxis, :], "x": x[np.newaxis, :], "Fe": np.array([[Fe]])})

print("Generated substitute files:")
print("  sounds/glockenspiel_mono.wav, sounds/desactive_mono.wav, signal_2sinus.mat")
