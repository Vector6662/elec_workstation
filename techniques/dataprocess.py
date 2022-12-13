import scipy
import numpy as np


# 平滑
def smooth(x, y, window_length=7):
    """
    采用的是S-G平滑，最小二乘法
    :param x:
    :param y:
    :param window_length:
    :return:
    """
    y = scipy.signal.savgol_filter(y, window_length, 3)
    return x, y


# 拟合
def fit(x, y):
    param = np.polyfit(x, y, 5)
    f = np.poly1d(param)
    return x, f(x)


# 导数
def cal_Nnd_deriv(x: list, y: list, deg: int):
    """
    离散点n阶导
    :param x:
    :param y:
    :param deg:
    :return:
    """
    if deg == 1:
        return cal_deriv(x, y)
    return cal_Nnd_deriv(x, cal_deriv(x, y), deg - 1)


def cal_deriv(x: list, y: list):
    """
    离散点一阶导数，参考：https://blog.csdn.net/goodCodeVsBadBs/article/details/108270333
    :param x:
    :param y:
    :return:
    """
    diff_x = []  # 用来存储x列表中的两数之差
    for i, j in zip(x[0::], x[1::]):
        diff_x.append(j - i)

    diff_y = []  # 用来存储y列表中的两数之差
    for i, j in zip(y[0::], y[1::]):
        diff_y.append(j - i)

    slopes = []  # 用来存储斜率
    for i in range(len(diff_y)):
        slopes.append(diff_y[i] / diff_x[i])

    deriv = []  # 用来存储一阶导数
    for i, j in zip(slopes[0::], slopes[1::]):
        deriv.append((0.5 * (i + j)))  # 根据离散点导数的定义，计算并存储结果
    deriv.insert(0, slopes[0])  # (左)端点的导数即为与其最近点的斜率
    deriv.append(slopes[-1])  # (右)端点的导数即为与其最近点的斜率

    for i in deriv:  # 打印结果，方便检查，调用时也可注释掉
        print(i)

    return deriv  # 返回存储一阶导数结果的列表


# 积分
def cal_integral(x, y):
    """
    离散点积分，累计梯形方式计算
    此外还有复合辛普森的方式，参考：https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simpson.html
    :param x:
    :param y:
    :return:
    """
    x, y = x[::-1], y[::-1]
    return scipy.integrate.cumulative_trapezoid(y, x, initial=0)
    # integrals = []
    # for i in range(len(y)):  # 计算梯形的面积，由于是累加，所以是切片"i+1"
    #     integrals.append(scipy.integrate.simpson(y[:i + 1], x[:i + 1])) #复合辛普森发
    #     integrals.append(scipy.integrate.trapz(y[:i + 1], x[:i + 1])) # 累计梯度
    #
    # return integrals


# 插值
def interpolate(x: list, y: list, n: int):
    # 采用的是b - spline样条函数
    # 报错：ValueError: Expect x to be a 1-D sorted array_like. 解决方案是是，x数据得递增排列
    x, y = x[::-1], y[::-1]
    x_interp = np.linspace(min(x), max(x), len(x) * n)
    y_interp = scipy.interpolate.make_interp_spline(x, y)(x_interp)
    return x_interp, y_interp
