import numpy as np
import scipy
import matplotlib.pyplot as plt

"""
傅里叶变换平滑和卷积平滑
"""


def moving_average(interval, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    re = np.convolve(interval, window, 'same')
    return re


def moving_fft(interval, windowsize):
    window = np.ones(int(windowsize))
    re = scipy.signal.fftconvolve(interval, window, 'same')
    return re


def fft_convolve(a, b):
    n = len(a) + len(b) - 1
    # 大于n的最小的2的整数次幂
    N = 2 ** (int(np.log2(n)) + 1)
    A = np.fft.fft(a, N)  # N为FFT长度，会自动补零
    B = np.fft.fft(b, N)
    return np.fft.ifft(A * B)[:n]


def convolve(x, h):
    L = len(x)
    M = len(h)
    N = L + M - 1
    x_p = np.pad(x, [M - 1, M - 1], mode='constant')
    index = np.arange(M)[::-1][None, :] + np.arange(N)[:, None]
    return np.dot(x_p[index], h)


x = [5, 6, 7, 8]
h = [1, 2, 3, 4]
convolve(x, h)
fig, (ori, fft, avg) = plt.subplots(3, 1)
t = np.linspace(-4, 6, 500)
y = np.sin(t) + np.random.randn(len(t)) * 0.1
fft_y = moving_fft(y, 30)
avg_y = moving_average(y, 30)

ori.set_title('origin')
ori.plot(t, y)

fft.plot(t, fft_y)
fft.set_title('fft')

avg.plot(t, avg_y)
avg.set_title('avg')
fig.show()

import differint.differint as df
