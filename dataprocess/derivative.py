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