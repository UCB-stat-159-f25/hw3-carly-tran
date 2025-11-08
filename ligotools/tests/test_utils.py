# ligotools/tests/test_utils.py
import numpy as np
from scipy.io import wavfile
from ligotools import utils as lu

def test_whiten():
    fs = 4096.0
    dt = 1.0 / fs
    t = np.arange(0, 1.0, dt)
    x = np.sin(2 * np.pi * 50 * t)

    psd_array = np.ones(len(x)//2 + 1)
    psd_func = lambda f: np.ones_like(f)

    try:
        # try callable version first
        y = lu.whiten(x, psd_func, dt)
    except TypeError:
        # fallback to array version
        y = lu.whiten(x, psd_array, dt)

    assert y.shape == x.shape
    assert np.isfinite(y).all()
    assert np.std(y) > 0


def test_write_wavfile(tmp_path):
    fs = 1024
    t = np.arange(0, 1.0, 1 / fs)
    x = np.sin(2 * np.pi * 10 * t)  # simple tone

    out = tmp_path / "test.wav"
    lu.write_wavfile(out, fs, x)

    # file exists and can be read back
    assert out.exists()
    rfs, data = wavfile.read(out)
    assert rfs == fs
    assert len(data) == len(x)
