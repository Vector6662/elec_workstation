# -*- coding: utf-8 -*-
# @Time    : 2022/3/19 9:59
# @Author  : Zhang Min
# @FileName: SG滤波.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

Size = 100
x = np.linspace(0, 2 * np.pi, 100)
data = np.sin(x) + np.random.random(100) * 2

# 利用SG滤波库savgol_filter
plt.plot(x, data, color = 'y', label = 'pre_filter data')
y = savgol_filter(data, 59, 3, mode = "nearest")
plt.plot(x, y, "b--", label = "sg")

# 自我实现代码 并比SG滤波代码库进行比较
# 3阶多项式
k = 3
# 滑动窗口大小
window_size = 59
# 前后各m个数据，共2m+1个数据，作为滑动窗口内滤波的值
m = int((window_size - 1) / 2)  # (59-1)  /2 = 29

# 计算 矩阵X 的值 ，就是将自变量x带进去的值算 0次方，1次方，2次方.....k-1次方,一共window_size行，k列
# 大小为（2m+1,k）
X_array = []
for i in range(window_size):  #
    arr = []
    for j in range(k):
        X0 = np.power(-m + i, j)
        arr.append(X0)
    X_array.append(arr)

X_array = np.mat(X_array)
# B = X*（X.T*X）^-1*X.T
B = X_array * (X_array.T * X_array).I * X_array.T
print(B.shape)

data = np.insert(data, 0, [data[0] for i in range(m)])  # 首位插入m-1个data[0]
data = np.append(data, [data[-1] for i in range(m)])  # 末尾插入m-1个data[-1]

# 取B中的第m行 进行拟合  因为是对滑动窗口中的最中间那个值进行滤波，所以只要获取那个值对应的参数就行， 固定不变
B_m = B[m]  # (1,59):(1,2m+1)
print(data.shape)
# 存储滤波值
y_array = []
# 对扩充的data 从第m个数据开始遍历一直到（data.shape[0] - m）  ：（第m个数据就是原始data的第1个，（data.shape[0] - m）为原始数据的最后一个
for n in range(m, data.shape[0] - m):
    y_true = data[n - m: n + m + 1]  # 取出真实y值的前后各m个，一共2m+1个就是滑动窗口的大小
    y_filter = np.dot(B_m, y_true)  # 根据公式 y_filter = B * X 算的  X就是y_true  (1,59) * (59,1) = (1,1)
    y_array.append(float(y_filter)) # float(y_filter) 从矩阵转为数值型

print(y_array)
# plt.plot(x, y_array,"g", label="o")
plt.legend()
plt.show()

