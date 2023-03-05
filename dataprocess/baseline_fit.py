import numpy as np
import math
import matplotlib.pyplot as plt


def Fun(N, deg):
    ''' 产生原曲线 sin函数
    '''
    # 产生带有高斯噪声的信号
    mid, sigma = 0, 0.3  # 设置均值和方差
    noise = np.random.normal(mid, sigma, N).reshape(N, 1)  # 生成SAMPLE_NUM个数据
    # 产生SAMPLE_NUM个序号(范围是2pi)
    x = np.arange(0, N).reshape(N, 1) / (N - 1) * (2 * math.pi)
    # generate y and y_noise, and both y's and y_noise's shape is (SAMPLE_NUM*1)
    y = np.sin(x)
    y_noise = np.sin(x) + noise
    return (x, y, y_noise)


def test_baseline_fit():
    SAMPLE_NUM = 100  # 要生成的sample个数
    M = 9  # 多项式阶数
    x, y, y_noise = Fun(SAMPLE_NUM, M)
    # 绿色曲线显示x - y，散点显示x - y_noise
    f1, = plt.plot(x, y, 'g', lw=4.0)  # , label = r'$y=\sin(x)$'
    f2, = plt.plot(x, y_noise, 'bo')  # ,label = r'$y=\sin(x)$ with noise'

    # generate Matrix X which has M order
    X = x
    for i in range(2, M + 1):
        X = np.column_stack((X, pow(x, i)))

    # add 1 on the first column of X, now X's shape is (SAMPLE_NUM*(M+1))
    X = np.insert(X, 0, [1], 1)
    # print(X)

    # calculate W, W's shape is ((M+1)*1)#
    # W=np.linalg.inv((X.T.dot(X))).dot(X.T).dot(y_noise)#have no regularization
    W = np.linalg.inv((X.T.dot(X)) + np.exp(-8) * np.eye(M + 1)).dot(X.T).dot(y_noise)  # introduce regularization
    y_estimate = X.dot(W)

    # 红色曲线显示x - y_estimate
    f3, = plt.plot(x, y_estimate, 'r', lw=4.0)
    plt.suptitle(r'最小二乘法多项式拟合原函数 $y=\sin(x)$', fontsize=10)
    plt.grid(color='gray')
    plt.grid(linewidth='1')
    plt.grid(linestyle='--')
    plt.legend([f1, f2, f3], [r'原函数 $y=\sin(x)$', r'$y=\sin(x)$ 叠加噪音', r'多项式拟合'], fontsize=10)
    plt.show()

def fit(x, y, m):
    """
    多项式最小二乘法实现
    :param x:输入
    :param y:目标输出
    :param m:多项式阶数
    :return:多项式系数
    """
    x = np.array(x)
    y = np.array(y)

    assert m <= x.shape[0], f"the number of m({m}) need less than x's size({x.shape[0]})"
    assert x.shape[0] == y.shape[0], f"the size of x({x.shape[0]}) must equal to y's size({y.shape[0]}"
    x_mat = np.zeros((x.shape[0], m+1))
    for i in range(x.shape[0]):
        x_mat_h = np.zeros((1, m+1))
        for j in range(m+1):
            x_mat_h[0][j] = x[i] ** (m-j)
        x_mat[i] = x_mat_h
    theta = np.dot(np.dot(np.linalg.inv(np.dot(x_mat.T, x_mat)), x_mat.T), y.T)
    f = np.poly1d(theta)
    return x, f(x)


def numpy_fit(x, y, deg: int):
    '''
    numpy的实现方式
    :param x:
    :param y:
    :param deg:
    :return:
    '''
    param = np.polyfit(x, y, deg)
    f = np.poly1d(param)
    return x, f(x)
