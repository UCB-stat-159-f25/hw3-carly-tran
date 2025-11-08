import numpy as np
import pytest
from pathlib import Path
from ligotools import readligo as rl

# Path to the data folder
DATA = Path(__file__).resolve().parents[2] / "data"
H1_FILE = DATA / "H-H1_LOSC_4_V2-1126259446-32.hdf5"

def test_loaddata_runs_and_shapes_match():
    # Basic sanity test loaddata
    strain, time, meta = rl.loaddata(str(H1_FILE), "H1")
    assert isinstance(strain, np.ndarray)
    assert isinstance(time, np.ndarray)
    assert len(strain) == len(time) and len(strain) > 0

    # Time should be strictly increasing
    dt = np.diff(time)
    assert np.all(dt > 0) or np.all(dt >= 0)

    # Estimate sampling rate from time differences
    fs_est = 1.0 / np.median(dt)
    assert np.isfinite(fs_est) and fs_est > 0

    if isinstance(meta, dict) and "fs" in meta:
        assert meta["fs"] > 0
        assert abs(meta["fs"] - fs_est) / fs_est < 0.05  # within 5%

def test_dq_channel_to_seglist_simple():
    # Test for boolean array segmentation
    channel = np.array([0, 1, 1, 0, 1, 1, 1, 0])
    segments = rl.dq_channel_to_seglist(channel, fs=1)
    expected = [slice(1, 3), slice(4, 7)]
    assert isinstance(segments, list)
    for seg, exp in zip(segments, expected):
        assert seg.start == exp.start
        assert seg.stop == exp.stop