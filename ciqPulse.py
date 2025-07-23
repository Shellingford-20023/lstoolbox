 import numpy as np
from scipy.integrate import cumulative_trapezoid
from itertools import zip_longest

dt = 0.5 # in unit of μs
phi0 = 0 # temporary
class Shapes:
    def __init__(self, tp, amp = 100, freq = [0, 0], phi0 = 0, tstart = 0, shape = 'rectangular', FM = 'linear', rp = None, **kwargs):
        self.dt = dt
        self.tstart = tstart
        self.tp = tp
        self.amp = amp
        self.freq = freq
        self.phi0 = phi0
        self.t = np.arange(0, tp+dt, dt)
        self.ti = self.t - self.tp/2 
        self.shape = shape
        self.FM = FM
        self.tfwhm = kwargs.get('tfwhm', 1)
        self.trunc = kwargs.get('trunc', 1)
        self.beta = kwargs.get('beta', 1)
        self.nwurst = kwargs.get('nwurst', 1)
        self.zerocross = kwargs.get('zerocross', 0.1)
        self.rp = kwargs.get('rp',1)
        # self.flip = flip
        # self.mwfreq = mwfreq

        self.transferfunction = kwargs.get('transfer function', 1)

        self.modamp = np.ones(len(self.t))
        self.modfreq = {}
        self.modphase = {}

        # if not hasattr(self, 'FM'):
        #     self.FM = "none"

        # if len(self.freq) == 1:
        #     # print('Must specify a range of frequency.')
        # # elif len(self.freq) == 0: 
        #     BW = 0
        # else: 
        #     BW = self.freq[-1] - self.freq[0]

        self.BW = self.freq[1] - self.freq[0]

        match self.FM:
            # case "none":
            #     modfreq = 0
            #     modphase = 0

            case "sech/tanh":
                BW_ = np.abs(np.max(self.BW) - np.min(self.BW))/np.tanh(self.beta/2)
                modfreq = (BW_/2)*np.tanh((self.beta/self.tp)*self.ti)
                modphase = 2*np.pi*(self.BW/2)*(self.tp/self.beta)*np.log(np.cosh((self.beta/self.tp)*self.ti))
                self.BW = BW_

            case "linear":
                k = self.BW/self.tp
                modfreq = k*self.ti
                modphase = 2*np.pi*((k/2)*self.ti**2)

            case "uniformQ": 
                modfreq = np.zeros(len(self.t))
                modfreq = (self.freq[-1] - self.freq[0])*(modfreq-1/2)
                modphase = np.zeros(len(self.t))
                modphase = 2*np.pi*cumulative_trapezoid(self.ti,modfreq)
        
        self.modfreq = modfreq
        self.modphase = modphase

        match self.shape:
            case "rectangular":
                A0 = np.ones(len(self.t))
        
            case "gaussian":
                A0 = self.modamp*np.exp(-(4*np.log(2)*self.ti**2)/self.tfwhm**2)

            case "sinc":
                x_ = 2*np.pi*ti/self.zerocross
                A0 = np.sin(x_)/x_
                A0[np.isnan(A0)] = 1

            case "WURST":
                A0 = 1 - np.abs(np.sin(np.pi*self.ti/self.tp))**self.nwurst

            case "sech/tanh":
                A0 = 1/(np.cosh(self.beta*self.ti/self.tp))
            # A0 = self.flip/(2*np.pi*cumulative_trapezoid(A0))
            
        self.modamp = A0*self.amp        
        self.totalphase = self.modphase + 2*np.pi*np.mean(self.freq)*self.t + self.phi0
        self.IQ = self.modamp*np.exp(-1j*self.totalphase)
    
    def resonator_comp(self):
        newaxis = nu0 + np.mean(self.freq)
        
        f = self.transferfunction[0] * 1e3
        H = self.transferfunction[1]
        
        if newaxis.min() < f.min() or newaxis.max() > f.max():
            raise ValueError("The Frequency swept width is greater than that of the resonator profile. Reduce the "
            "frequency sweep width of the pulse or increase the frequency sweep width of the "
            "resonator profile ")
        
        if not np.any(np.isreal(H)):
            H = np.abs(H)
            transferfunction = interp1d(f, H)(newaxis)
        # Calculate for user specified resonator frequency
        elif hasattr(self, 'resonator_frequency'):
            f0 = self.resonator_frequency * 1e3
            QL = self.resonator_ql
            profile = np.abs(1 / (1 + 1j * QL * (newaxis / f0 - f0 / newaxis)))
        else:
            raise AttributeError('Pulse object must have `resonator_frequency` or `profile` defined in kwargs')

        if self.fm_func.__name__ == 'uniformq' or self.shape == 'sech/tanh':
            profile *= A0

        int = cumtrapz(profile ** -2, nu0, initial=0)
        tf = self.time[-1] * int / int[-1]
        nu_adapted = pchip_interpolate(tf, nu0, self.time)

        self.frequency_modulation = nu_adapted
        self.phase = 2 * np.pi * cumtrapz(self.frequency_modulation, self.time, initial=0)
        self.phase += np.abs(np.min(self.phase))

        if self.fm_func.__name__ == 'uniformq' or self.shape == 'sech/tanh':
            self.amplitude_modulation = pchip_interpolate(nu0, A0, nu_adapted)

        pass