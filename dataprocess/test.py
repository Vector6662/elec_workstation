import numpy as np
import scipy
import matplotlib.pyplot as plt

def moving_average(interval, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    re = np.convolve(interval, window, 'same')
    return re

def moving_fft(interval, windowsize):
    window = np.ones(int(windowsize))
    re = scipy.signal.fftconvolve(interval,window, 'same')
    return re

fig, (ori,fft,avg)= plt.subplots(3,1)
t = np.linspace(-4, 6, 500)
y = np.sin(t) + np.random.randn(len(t)) * 0.1
fft_y = moving_fft(y,30)
avg_y = moving_average(y,30)

ori.set_title('origin')
ori.plot(t,y)

fft.plot(t,fft_y)
fft.set_title('fft')

avg.plot(t,avg_y)
avg.set_title('avg')
fig.show()

import differint.differint as df

