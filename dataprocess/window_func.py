# 窗函数

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import mpl
from scipy.fftpack import fft

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


def windows_plot():
    """
    各种窗函数时域、频域图
    :return:
    """

    N = 50
    # 采样点选择1400个，由于设置的信号频率份量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，因此这里设置采样频率为1400赫兹（即一秒内有1400个采样点，同样意思的）
    x = np.linspace(0, 10, N)

    # 设置须要采样的信号，频率份量有200，400和600
    windows = {'hanning': np.hanning, 'hamming': np.hamming, 'bartlett': np.bartlett, 'blackman': np.blackman}

    for key in windows:
        y = windows[key](x.size)
        fft_y = fft(y)  # 快速傅里叶变换
        x = np.arange(N)  # 频率个数
        half_x = x[range(int(N / 2))]  # 取一半区间

        abs_y = np.abs(fft_y)  # 取复数的绝对值，即复数的模(双边频谱)
        angle_y = np.angle(fft_y)  # 取复数的角度
        normalization_y = abs_y / N  # 归一化处理（双边频谱）
        normalization_half_y = normalization_y[range(int(N / 2))]  # 因为对称性，只取一半区间（单边频谱）

        plt.subplot(1, 2, 1)
        plt.plot(x, y, label=key)
        plt.subplot(1, 2, 2)
        plt.plot(half_x, normalization_half_y, label=key)
    plt.subplot(1, 2, 1)
    plt.xlabel('sample')
    plt.ylabel('amplitude')
    plt.title('原始波形')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.title('单边振幅谱(归一化)')
    plt.legend()
    plt.show()

def window_anaylse():
    """
    加窗分析
    :return:
    """
    sampling_rate = 8000
    fft_size = 512
    t = np.arange(0, 1.0, 1.0 / sampling_rate)
    x = np.sin(2 * np.pi * 200 * t) + 2 * np.sin(2 * np.pi * 300 * t)

    xs = x[:fft_size]
    ys = xs * np.hamming(fft_size)
    # 时域图
    plt.plot(t[:fft_size], ys, label='信号')
    plt.plot(t[:fft_size], np.hanning(fft_size), label='hamming窗')
    plt.title('加hamming窗时域图')
    plt.xlabel('time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

    # 频域图
    xf = np.fft.rfft(xs) / fft_size
    yf = np.fft.rfft(ys) / fft_size
    freqs = np.linspace(0, sampling_rate / 2, int(fft_size / 2 + 1))
    # xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    # yfp = 20 * np.log10(np.clip(np.abs(yf), 1e-20, 1e100))
    xfp = np.abs(xf)
    yfp = np.abs(yf)
    plt.figure(figsize=(8, 4))
    # plt.title(u"200Hz和300Hz的波形和频谱")
    plt.plot(freqs, xfp, label=u"原信号")
    plt.plot(freqs, yfp, label=u"加入bartlett窗")
    plt.legend()
    plt.xlabel(u"Frequency")
    plt.ylabel('Amplitude')

    a = plt.axes([.4, .2, .4, .4])
    a.plot(freqs, xfp, label=u"原信号")
    a.plot(freqs, yfp, label=u"bartlett窗")
    a.set_xlim(100, 400)
    # a.set_ylim(-40, 0)
    plt.show()
