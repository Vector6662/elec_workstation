import scipy
import numpy as np
import statsmodels.api as sm


# 平滑
def smooth(x, y, window_length=7, polyorder=3):
    """
    采用的是S-G平滑，最小二乘法
    :param polyorder: 
    :param x:
    :param y:
    :param window_length:
    :return: y
    """
    return scipy.signal.savgol_filter(y, window_length, polyorder)


# 拟合
def lsq_fit(x, y, deg: int):
    """
    多项式最小二乘拟合
    :param x:
    :param y:
    :param deg: 阶数
    :return:
    """
    param = np.polyfit(x, y, deg)
    f = np.poly1d(param)
    return x, f(x)


def ols_fit(x, y, deg: int):
    """
    普通最小二乘拟合
    :param deg:
    :param x:
    :param y:
    :return:
    """
    # todo 这里的实现改一下，应该是加入正则项后的
    x_const = sm.add_constant(x)
    model = sm.OLS(y, x_const)
    results = model.fit()
    return x, results.predict(x_const)
    # x,y = np.array(x), np.array(y)
    # W = np.linalg.inv(x.T.dot(x)+np.exp(-8) * np.eye(6+1)).dot(x.T).dot(y)
    # return x.dot(W)


# 导数
def n_derivative(x: list, y: list, deg: int):
    """
    离散点n阶导
    :param x:
    :param y:
    :param deg:
    :return: y
    """
    if deg == 1:
        return derivative(x, y)
    return n_derivative(x, derivative(x, y), deg - 1)


def derivative(x: list, y: list):
    """
    离散点一阶导数，参考：https://blog.csdn.net/goodCodeVsBadBs/article/details/108270333
    :param x:
    :param y:
    :return: y
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

    # for i in deriv:  # 打印结果，方便检查，调用时也可注释掉
    #     print(i)

    return deriv  # 返回存储一阶导数结果的列表


# 积分
def integrate_trapezoid(x, y):
    """
    离散点积分，累计梯形方式计算
    此外还有复合辛普森的方式，参考：https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simpson.html
    :param x:
    :param y:
    :return:
    """
    x, y = x[::-1], y[::-1]
    return scipy.integrate.cumulative_trapezoid(y, x, initial=0)  # 复合梯形法则
    # integrals = []
    # for i in range(len(y)):  # 计算梯形的面积，由于是累加，所以是切片"i+1"
    #     integrals.append(scipy.integrate.simpson(y[:i + 1], x[:i + 1])) #辛普森法
    #     integrals.append(scipy.integrate.trapz(y[:i + 1], x[:i + 1])) # 梯形
    #
    # return integrals


def integrate_simpson(x, y):
    x, y = x[::-1], y[::-1]
    integrals = []
    for i in range(len(y)):  # 计算梯形的面积，由于是累加，所以是切片"i+1"
        integrals.append(scipy.integrate.simpson(y[:i + 1], x[:i + 1]))  # 辛普森法

    return integrals


# 插值
def interpolate(x: list, y: list, density: int):
    # density:设置插入密度
    # 采用的是b - spline样条函数
    # 报错：ValueError: Expect x to be a 1-D sorted array_like. 解决方案是是，x数据得递增排列
    # todo 有些数据本身就是递增的
    x, y = x[::-1], y[::-1]
    x_interp = np.linspace(min(x), max(x), len(x) * density)
    y_interp = scipy.interpolate.make_interp_spline(x, y)(x_interp)
    return x_interp, y_interp
