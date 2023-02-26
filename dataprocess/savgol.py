# -*- coding: utf-8 -*-
# @Time    : 2022/3/19 9:59
# @Author  : Zhang Min
# @FileName: SG滤波.py
# 参考：https://blog.csdn.net/weixin_45929124/article/details/123601803
import time

import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.metrics import mean_squared_error


def savgol_filter(K, N, y):
    # 前后各m个数据，共2m+1个数据，作为滑动窗口内滤波的值
    m = int((N - 1) / 2)  # (59-1)  /2 = 29

    # 计算 矩阵X 的值 ，就是将自变量x带进去的值算 0次方，1次方，2次方.....k-1次方,一共window_size行，k列
    # 大小为（2m+1,k）
    X_array = []
    for i in range(N):  #
        arr = []
        for j in range(K):
            X0 = np.power(-m + i, j)
            arr.append(X0)
        X_array.append(arr)

    X_array = np.mat(X_array)
    # B = X*（X.T*X）^-1*X.T
    B = X_array * (X_array.T * X_array).I * X_array.T
    # print(B.shape)

    y = np.insert(y, 0, [y[0] for i in range(m)])  # 首位插入m-1个data[0]
    y = np.append(y, [y[-1] for i in range(m)])  # 末尾插入m-1个data[-1]

    # 取B中的第m行 进行拟合  因为是对滑动窗口中的最中间那个值进行滤波，所以只要获取那个值对应的参数就行， 固定不变
    B_m = B[m]  # (1,59):(1,2m+1)
    # print(y.shape)
    # 存储滤波值
    y_array = []
    # 对扩充的data 从第m个数据开始遍历一直到（data.shape[0] - m）  ：（第m个数据就是原始data的第1个，（data.shape[0] - m）为原始数据的最后一个
    for n in range(m, y.shape[0] - m):
        y_true = y[n - m: n + m + 1]  # 取出真实y值的前后各m个，一共2m+1个就是滑动窗口的大小
        y_filter = np.dot(B_m, y_true)  # 根据公式 y_filter = B * X 算的  X就是y_true  (1,59) * (59,1) = (1,1)
        y_array.append(float(y_filter))  # float(y_filter) 从矩阵转为数值型

    # print(y_array)
    return y_array


Size = 100
x = np.linspace(0, 2 * np.pi, Size)
data = np.sin(x) + np.random.randn(len(x)) * 2
# data = np.sin(2 * np.pi * 50 * x) + np.cos(2 * np.pi * 30 * x) + np.random.randn(len(x)) * 2 + x
# 真实值
plt.subplot(3, 1, 1)
plt.title('origin data')
plt.plot(x, data, color='y')


# 利用SG滤波库savgol_filter
plt.subplot(3, 1, 2)
plt.title('scipy.signal.savgol_filter')
start_time = time.time()
y_scipy = scipy.signal.savgol_filter(data, 59, 3, mode="nearest")
end_time = time.time()
print(f'Execution time(scipy): {end_time - start_time}')
plt.plot(x, y_scipy, "b--", label="sg")

# 自我实现代码 并比SG滤波代码库进行比较
# 3阶多项式
k = 3
# 滑动窗口大小
window_size = 59

start_time = time.time()
y_smooth = savgol_filter(k, window_size, data)
end_time = time.time()
print(f'Execution time: {end_time - start_time}')
plt.subplot(3, 1, 3)
plt.title('smooth')
plt.plot(x, y_smooth, "b--", color='g')
plt.show()

mse = mean_squared_error(y_scipy, y_smooth)
print('mse:',mse)