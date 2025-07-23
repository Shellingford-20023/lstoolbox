import numpy as np
from itertools import zip_longest
import json
import os
import struct

class Exp:
    def __init__(self, pulses, dim = [1, 0], ):
        pass
    
def Preview(pulses):
    dt = pulses[0].dt
    I = []
    Q = []
    delays = [None]*(len(pulses)-1)
    for idx in range(0, len(pulses)-1):
        dxlen = (pulses[idx+1].tstart - (pulses[idx].tstart+pulses[idx].tp))/dt + 1
        delay = np.zeros(int(dxlen))
        delays[idx] = delay
        I = []
        Q = []
    for p, d in zip_longest(pulses, delays):
        if p is not None:
            I_ = p.IQ.real
            Q_ = p.IQ.imag
            I.append(I_)
            Q.append(Q_)
        if d is not None:
            I.append(d)
            Q.append(d)
    I_flat = [block for subblocks in I for block in subblocks]
    I = np.array(I_flat)
    Q_flat = [block for subblocks in Q for block in subblocks]
    Q = np.array(Q_flat)
    t = np.arange(0, len(I)*dt, dt)
    return t, I, Q, delays

def ciqRead(filename):
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

def GenAWGData(I, Q, filename):
    list_I = I.tolist()
    list_Q = Q.tolist()
    with open(filename, 'bw') as wf:
        wf.write(b'AWGw')                                               #文件头标识符
        wf.write(struct.pack('I', len(list_I) * 8))                          #I路数据的长度
        wf.write(struct.pack('I', len(list_Q) * 8))                          #Q路数据的长度
        #wf.write(struct.pack('{}d'.format(len(list_I)), *list_I))        #写入的数据。
        for i, q in zip(list_I, list_Q):
            wf.write(struct.pack('d', i))
            wf.write(struct.pack('d', q))
        
def ShowAWGData(filename):
    # file_name = "E:\\AWGWaveData.wave"

    # 打开文件并读取所有数据
    with open(filename, "rb") as file:
        file_data = file.read()

    # 按8字节为一个数值进行解析
    start_byte = 12
    num_values = (len(file_data) - start_byte) // 16
    I_List = []
    Q_List = []
    for i in range(num_values):
        # 从文件数据中读取8字节,并使用struct.unpack将其解析为一个 float64 类型的数值
        value_bytes = file_data[start_byte + i * 16:start_byte + i * 16 + 8]
        value = struct.unpack("d", value_bytes)[0]
        I_List.append(value)
        value_bytes = file_data[start_byte + i * 16 + 8:start_byte + i * 16 + 16]
        value = struct.unpack("d", value_bytes)[0]
        Q_List.append(value)

    #print(I_List,Q_List)    
    m_sampleRate = 2    
    # 设置 x 坐标
    x_values = [i * 1 / m_sampleRate for i in range(num_values)]  # 生成时间列表
    return x_values, I_List, Q_List
  