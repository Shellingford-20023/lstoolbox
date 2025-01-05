import numpy as np

# % Now...how to get S = 1/2 and I = 1/2? 
# % dimension = (2S+1)(2I+1) 

def sop(S):
    nstates = 2*S+1
    # Allocate eigen states in Sz
    eigSz = np.zeros([nstates, nstates] + np.diag(np.ones(nstates),1))
    # projection of angular moment?
    m = np.arange(-S,S+1,1);
    m = np.sort(m,'descend');


