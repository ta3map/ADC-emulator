import pandas as pd
import numpy as np
from scipy.signal import resample_poly
from scipy.signal import resample

def rec(v, samples, quant_levels, target_fs):
    folder = '/content/ADC_simulator/'
    #folder = r'C:\Users\Azat\Documents\Digital Signal Processing\Lab. 2\ADC_simulator_2021/'
    path = folder + 'data/data'+ str(v) +'_v2'

    def is_int(x):
        try:
             int(x)
             return True
        except:
             return False
         
    def quantization(signal, quant_levels):
        quanted = np.zeros(np.size(signal));
        for i in range(len(quant_levels)):
            quanted[signal>quant_levels[i]] = quant_levels[i]; 
        return quanted
    
    def change_size(signal, samples):
        size_dif = len(signal) - samples
        if size_dif<0:
            std_y = np.std(signal)
            mean_y = np.mean(signal)
            a = std_y/2
            nothing = a*np.random.rand(np.abs(size_dif))+mean_y-a/2
            output = np.append(signal, quantization(nothing, quant_levels))
        else:                
            output = quanted[0:samples]
        return output
        
    y = pd.read_csv(path,  header=None).to_numpy().flatten()
    original_fs, signal = int(y[0]), y[1:]
    
 
    
    least_common_divisor = np.lcm(original_fs,target_fs)
    upsample_factor = least_common_divisor/original_fs
    downsample_factor = least_common_divisor/target_fs    

    
    assert is_int(downsample_factor) and is_int(upsample_factor), f"Unfortunately we cannot sample with the requested sampling frequency: {target_fs}. Please try some other value."
    #resampled = resample_poly(signal, upsample_factor, downsample_factor)
    resampled = resample_poly(signal, upsample_factor, 1)
    resampled = resampled[0:len(resampled):int(downsample_factor)]

    quanted = quantization(resampled, quant_levels)
    output = change_size(quanted, samples)

    return output
