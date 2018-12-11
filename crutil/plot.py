import numpy as np
import matplotlib.pyplot as plt

def freq_response(w, *args, fig=None, ax=None, analog=False, Hz=True, sfreq=None, db=True, degrees=False, \
                       grid=True, logx=False):

    # By default, create a new plot, but allow adding to existing plots if more convenient.
    if fig is None and ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    elif fig is None:
        fig = ax.get_figure()
    elif ax is None:
        ax = fig.gca()
    ax2 = ax.twinx()

    if sfreq and analog:
        raise ValueError("Analog and sfreq are mutually exclusive")

    if analog:
        if Hz:
            f = w/(2*np.pi) # Normalize to Hz
            ax.set_xlabel('Frequency (Hz)')
        else:
            f = w # Keep in radians
            ax.set_xlabel('Frequency (omega)')
    else:
        if sfreq:
            f = (sfreq)*(w/(2*np.pi)) # Normalize to Hz if provided, as
            # we are typically not interested in radian sampling rates.
            ax.set_xlabel('Frequency (Hz)')
        else:
            f = w # Normalize to pi/Nyquist freq if sfreq was not provided.
            ax.set_xlabel('Frequency (rad/sample)')

    mag_args = []
    if db:
        mag_repr = lambda x: 20*np.log10(abs(x))
        ax.set_ylabel('Amplitude (dB)', color='b')
    else:
        mag_repr = lambda x: abs(x)
        ax.set_ylabel('Amplitude (raw)', color='b')
    for x in range(0, len(args), 2):
        mag_args = mag_args + [f, mag_repr(args[x]), args[x + 1][0]]

    phase_args = []
    if degrees:
        phase_repr = lambda x: 180*np.unwrap(np.angle(x))/np.pi
        ax2.set_ylabel('Phase (degrees)', color='r')
    else:
        phase_repr = lambda x: np.unwrap(np.angle(x))
        ax2.set_ylabel('Phase (rad)', color='r')
    for x in range(0, len(args), 2):
        phase_args = phase_args + [f, phase_repr(args[x]), args[x + 1][1]]

    if logx:
        ax.set_xscale('log')

    if grid:
        # TODO: Make color of the grid and labels programmable?
        ax.xaxis.grid(True, which='both', linestyle=":", linewidth=0.5)
        ax.yaxis.grid(True, which='both', color='b', linestyle=":", linewidth=0.5)
        ax2.yaxis.grid(True, which='both', color='r', linestyle=":", linewidth=0.5)

    ax.plot(*mag_args)
    ax2.plot(*phase_args)
    return (fig, ax, ax2)


# Small wrapper for plot_freq_response that will do phase unwrapping.
# **kwargs is anything plot_freq_response takes, though some don't really
# make sense.
# Multiple inputs MUST be the same length as each other- limitation of
# what plot_freq_response was intended to measure.
def fft(*args, **kwargs):
    sig_args = []
    for x in range(0, len(args), 2):
        fft_sig = np.fft.fft(args[x])
        uw_fft_sig = np.fft.fftshift(fft_sig)
        sig_args = sig_args + [uw_fft_sig, args[x + 1]]

    freqs = 2*np.pi*np.fft.fftshift(np.fft.fftfreq(len(uw_fft_sig)))
    return freq_response(freqs, *sig_args, **kwargs)


# Generate l samples starting at t=0 for a given sampling frequency.
def simspace(l, fs):
    return np.linspace(0, l/fs, l + 1, endpoint=True)[:-1]
