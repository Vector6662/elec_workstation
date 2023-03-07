
# 线性趋势项扣除仿真，参考：https://zhuanlan.zhihu.com/p/336228933、
# https://blog.csdn.net/qq_42233059/article/details/126449677
# https://blog.csdn.net/weixin_42918498/article/details/120875063
import random

import numpy as np
import os

import numpy as np
import pylab as pl
import scipy.signal as signal
import matplotlib.pyplot as plt

# 模拟1
# t = np.arange(0, 100, 1)
# x = 3 * np.sin(5 * t) + np.cos(3 * t) + np.random.randn(len(t)) + t / 10
# d_x = signal.detrend(x)
# plt.subplot(2, 1, 1)
# plt.title('baseline and trend')
# plt.plot(t, x, label='data')
# plt.plot(t, x - d_x, label='baseline')
# plt.legend()
# plt.subplot(2, 1, 2)
# plt.title('correct')
# plt.plot(t, d_x, color='#8FBC8A')
# plt.show()


# 模拟2
from numpy.random import default_rng

rng = default_rng()
npoints = 1000
t = np.linspace(0, 1000, npoints)
noise = rng.standard_normal(npoints)
x = 3 + 2 * np.linspace(0, 1, npoints) + noise + np.sin(npoints)
d_x = signal.detrend(x)
(d_x - noise).max()
plt.subplot(2,1,1)
plt.title('baseline and trend')
plt.plot(t, x,label='data')
plt.plot(t, x - d_x,label='baseline')
plt.legend()

plt.subplot(2,1,2)
plt.title('correct')
plt.plot(t, d_x, color='#8FBC8F')
plt.show()
