import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

path = '/usr/share/fonts/truetype/SimHei.ttf'
fontprop = fm.FontProperties(fname=path, size=13)

SAMPLE_NUM = 100  # 要生成的sample个数
M = 9  # 多项式阶数


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
plt.suptitle(r'最小二乘法多项式拟合原函数 $y=\sin(x)$', fontsize=10, fontproperties=fontprop)
plt.grid(color='gray')
plt.grid(linewidth='1')
plt.grid(linestyle='--')
plt.legend([f1, f2, f3], [r'原函数 $y=\sin(x)$', r'$y=\sin(x)$ 叠加噪音', r'多项式拟合'], fontsize=10, prop=fontprop)
plt.show()
