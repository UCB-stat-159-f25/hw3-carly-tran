from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

# whiten the data 
def whiten(strain, psd, dt):
    hf = np.fft.rfft(strain)
    psd_safe = np.where(psd <= 0, np.inf, psd)
    white_hf = hf / np.sqrt(psd_safe / (dt / 2.0))
    return np.fft.irfft(white_hf, n=len(strain))

def reqshift(data, fshift, fs):
    t = np.arange(len(data)) / float(fs)
    return np.real(data * np.exp(1j * 2.0 * np.pi * fshift * t))

# keep data in integer limits and write to the wavfile
def write_wavfile(path, fs, data):
    path = Path(path)
    x = np.asarray(data)
    if np.issubdtype(x.dtype, np.floating):
        m = float(np.max(np.abs(x))) or 1.0
        x = (x / m * 32767.0).astype(np.int16)
    else:
        x = x.astype(np.int16)
    wavfile.write(str(path), int(fs), x)

# plotting function 
def plot_psd_section(time, strain, fs, eventname, window_len=4.0, overlap=2.0, plottype='png', outdir='figures'):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    nperseg = int(window_len * fs)
    noverlap = int(overlap * fs)
    freqs, psd = signal.welch(strain, fs=fs, window='tukey', nperseg=nperseg, noverlap=noverlap)
    asd = np.sqrt(psd)
    plt.figure(figsize=(7, 4))
    plt.loglog(freqs, asd)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'ASD [strain$/\sqrt{\mathrm{Hz}}$]')
    plt.title(f'{eventname} — Amplitude Spectral Density')
    plt.grid(True, which='both', alpha=0.3)
    outpath = outdir / f'{eventname}_psd.{plottype}'
    plt.tight_layout(); plt.savefig(str(outpath), dpi=150, bbox_inches='tight'); plt.close()
    return freqs, psd
