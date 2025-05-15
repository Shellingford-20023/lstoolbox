from functools import reduce
from pathlib import Path
from itertools import accumulate
import numpy as np
# from numpy.fft import fft, fftshift
from scipy.sparse import csr_matrix, kron
from scipy.interpolate import interp1d
import math

def lorentzian(x, x0, A, gamma, c):
    return A * (gamma**2 / ( gamma**2 + (x - x0)**2)) + c

def gaussian(x, x0, sigma, A, c):
    return A*1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x - x0)**2/(2*sigma**2)) + c

def nextpow2(x):
    """Clone of MATLAB's nextpow function"""
    return 1 if x == 0 else int(np.ceil(np.log2(x)))

def tohalf(x):
    return math.floor(x * 2) / 2

def fdaxis(dt, zf = 2**10):
    zf = 2**16
    # gx = (np.fft.fftshift(np.fft.fft(vt, zf)))
    nyquistfreq = 1/(2*dt)
    unitax = 2/zf*(np.arange(0,zf,1) - np.round(zf/2))
    ftax = nyquistfreq*unitax
    return ftax
       