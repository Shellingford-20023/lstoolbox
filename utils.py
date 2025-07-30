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

def fdaxis(dt, npts):
    nyquistfreq = 1/(2*dt)
    unitax = 2/npts*(np.arange(0,npts,1) - np.round(npts/2))
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

def basecorr(data, n, dim=1, region=None):
    """
    Perform 1D polynomial fitting along columns (dim=1) or rows (dim=2).

    Parameters:
        data (2D np.array): The input matrix.
        n (int): Degree of the polynomial.
        dim (int): Dimension to fit along: 1 (columns) or 2 (rows).
        region (1D np.array or list of indices): Optional, indices to use for fitting.

    Returns:
        baseline (2D np.array): The fitted polynomial baseline.
    """
    data = np.asarray(data)
    # Transpose if we are fitting along rows
    transpose = False
    if dim == 2:
        data = data.T
        transpose = True
    # Build design matrix D
    x = np.linspace(-1, 1, data.shape[0])  # centered and scaled
    D = np.column_stack([x**i for i in range(n + 1)])  # Shape: (rows, n+1)
    # Fit polynomials
    if region is None:
        # Fit to all rows
        p, _, _, _ = np.linalg.lstsq(D, data, rcond=None)  # Shape: (n+1, cols)
    else:
        region = np.asarray(region).flatten()
        p, _, _, _ = np.linalg.lstsq(D[region, :], data[region, :], rcond=None)
    # Evaluate baseline
    baseline = D @ p  # Shape: same as data
    # Transpose back if needed
    if transpose:
        baseline = baseline.T

    return baseline

def mypalette(color):
    match color:
        case 'gray':
            colorcode = [0.65, 0.65, 0.65]
        case 'red':
            colorcode = [0.8500, 0.3250, 0.0980]
        case 'yellow':
            colorcode = [0.9290, 0.6940, 0.1250]
        case 'pumpkin':
            colorcode = [1.0000, 0.4588, 0.0941]
        case 'pink':
            colorcode = [1.0000, 0.7137, 0.8588]

        case 'green':
            colorcode = [0.1333, 0.5451, 0.1333]
        case 'teal':
            colorcode = [0.0706, 0.7608, 0.6784]
        case 'ciq blue, dark':
            colorcode = [0.1412, 0.3255, 0.6392]
        case 'ciq blue, light':
            colorcode = [0.0471, 0.6118, 0.8941]
        case 'cyan':
            colorcode = [0.0471, 0.6118, 0.8941]
            
        case 'periwinkle':
            colorcode = [0.7451, 0.5765, 0.8941]
    return colorcode
