import numpy as np
import matplotlib.pyplot as plt


# 自动峰检测算法，参考：https://zhuanlan.zhihu.com/p/549588865

def AMPD(data):
    """
    实现AMPD算法
    :param data: 1-D numpy.ndarray
    :return: 波峰所在索引值的列表
    """
    p_data = np.zeros_like(data, dtype=np.int32)
    count = data.shape[0]
    arr_rowsum = []
    for k in range(1, count // 2 + 1):
        row_sum = 0
        for i in range(k, count - k):
            if data[i] > data[i - k] and data[i] > data[i + k]:
                row_sum -= 1
        arr_rowsum.append(row_sum)
    min_index = np.argmin(arr_rowsum)
    max_window_length = min_index
    for k in range(1, max_window_length + 1):
        for i in range(k, count - k):
            if data[i] > data[i - k] and data[i] > data[i + k]:
                p_data[i] += 1
    return np.where(p_data == max_window_length)[0]


def sim_data():
    N = 1000
    x = np.linspace(0, 200, N)
    y = 2 * np.cos(2 * np.pi * 300 * x) \
        + 5 * np.sin(2 * np.pi * 100 * x) \
        + np.random.randn(N)
    return y

def wav_data():
    # 数据来源：https://github.com/LXP-Never/blog_data/tree/master/machine_learning_date
    import scipy.io.wavfile as wf
    sample_rate, noised_sigs = wf.read('../实验数据/music.wav')
    print(sample_rate)  # sample_rate：采样率44100
    print(noised_sigs.shape)  # noised_sigs:存储音频中每个采样点的采样位移(220500,)
    times = np.arange(noised_sigs.size) / sample_rate
    return noised_sigs[:3000]


def vis():
    y = sim_data()
    # y = wav_data()
    plt.plot(range(len(y)), y)
    px = AMPD(y)
    plt.scatter(px, y[px], color="red")

    a = plt.axes([.4, .2, .4, .4])
    a.scatter(px, y[px], color="red")
    a.plot(range(len(y)), y, label=u"原信号", color='green')
    a.set_xlim(100, 300)

    plt.show()


# vis()
