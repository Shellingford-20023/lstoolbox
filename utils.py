import numpy as np
import math
import json

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
       
def ciqread(filename):
        with open(filename, "r") as file:
                data = json.load(file)  # Load JSON content as a Python dictionary

        setting = data["setting"]
        npts2D = len(data["dataStore"]["lineDataList"])

        if npts2D == 1:
                I_ = np.array(data["dataStore"]["lineDataList"][0]["ReData"])
                Q_ = np.array(data["dataStore"]["lineDataList"][0]["ImData"])
                I = I_[:,1]
                Q = Q_[:,1]
                ax = Q_[:,0]
                return ax, I, Q, setting
        else:
                npts1D = len(data["dataStore"]["lineDataList"][0]["ReData"])
                ax = np.zeros((npts2D,npts1D))
                I = np.zeros((npts2D,npts1D))
                Q = np.zeros((npts2D,npts1D))
                for n in np.arange(0, npts2D-1, 1):  
                        I_ = 1*np.array(data["dataStore"]["lineDataList"][n]["ReData"])
                        Q_ = 1*np.array(data["dataStore"]["lineDataList"][n]["ImData"]) 
                        I[n,:] = I_[:,1]
                        Q[n,:] = Q_[:,1] 
                        ax[n,:] = I_[:,0]
        return ax, I, Q, setting 

def mypalette(color):
    match color:
        case 'ciq blue, dark':
            colorcode = [0.1412, 0.3255, 0.6392]
        case 'ciq blue, light':
            colorcode = [0.0471, 0.6118, 0.8941]
        case 'forest green':
            colorcode = [0.1333, 0.5451, 0.1333]
        case 'gray':
            colorcode = [0.65, 0.65, 0.65]
        case 'pumpkin':
            colorcode = [1.0000, 0.4588, 0.0941]
            
    return colorcode
