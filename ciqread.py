import json 
import numpy as np

class ciqread():
    def __init__(self, filename):
        self.filename = filename

    def getdata(self):
        with open(self.filename, "r") as file:
                data = json.load(self.filename)  # Load JSON content as a Python dictionary

        setting = data["setting"]
        npts2D = len(data["dataStore"]["lineDataList"])

        if npts2D == 1:
                I_ = np.array(data["dataStore"]["lineDataList"][0]["ReData"])
                Q_ = np.array(data["dataStore"]["lineDataList"][0]["ImData"])
                I = I_[:,1]
                Q = Q_[:,1]
                ax = Q_[:,0]
                return ax, I, Q 
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
                return npts2D, ax, I, Q    
        

# ImData_= data["dataStore"]["lineDataList"][0]['ImData']
# ax = [col[0] for col in ImData_]
# ImData = [col[1] for col in ImData_]
# ReData_= data["dataStore"]["lineDataList"][0]['ReData']
# ax = [col[0] for col in ReData_]
# ReData = [col[1] for col in ReData_]