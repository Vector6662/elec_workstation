"""
误差评估
参考：https://cloud.tencent.com/developer/article/1773823
"""
import math
import os
import random
import matplotlib.pyplot as plt

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate(y_actual: list, y_predicted: list, actual_name=None, predict_name=None, title=None):
    """

    :param y_actual:
    :param y_predicted:
    :param actual_name: 实际曲线名称
    :param predict_name: 预测曲线名称
    :param title: 标题，比如基线拟合，插值等
    :return: text，误差评估格式化后的文本；evalDict，字典格式结果
    """
    y_actual, y_predicted = np.asarray(y_actual), np.asarray(y_predicted)
    mae = mean_absolute_error(y_actual, y_predicted)
    mape = np.mean(np.abs((y_predicted - y_actual) / y_actual)) * 100
    mse = mean_squared_error(y_actual, y_predicted)
    sse = np.sum((y_actual - y_predicted) ** 2)
    ssr = np.sum((y_predicted - np.mean(y_actual)) ** 2)
    sst = np.sum((y_actual - np.mean(y_actual)) ** 2)
    r2 = 1 - sse / sst  # r2_score(y_actual, y_predicted, multioutput='raw_values')
    rmse = np.sqrt(mean_squared_error(y_actual, y_predicted))
    count = np.size(y_predicted)
    predictionMean = np.mean(y_predicted)
    yMean = np.mean(y_actual)
    try:
        r = math.sqrt(r2)
    except ValueError:
        r = np.nan

    predict_name, actual_name = 'predict' if predict_name is None else predict_name, 'actual' if actual_name is None else actual_name
    text = '' if title is None else title
    text += '\n{} ---> {}\n'.format(predict_name, actual_name)
    text += '====================================\n'
    text += 'count: {}, prediction_mean: {}, y_mean: {}\n' \
            'MAE(平均绝对误差): {}\nMAPE(平均绝对百分误差): {}%\nMSE(均方误差):{}\nR(多重相关系数): {}\nR2(判定系数): {}\n' \
            'RMSE(均方根误差): {}\nSSE(误差平方和): {}\nSSR(回归平方和): {}\nSST: {}' \
        .format(count, np.round(predictionMean, 4), np.round(yMean, 4), np.round(mae, 4), np.round(mape, 4),
                np.round(mse, 4),
                np.round(r, 4), np.round(r2, 4), np.round(rmse, 4), np.round(sse, 4), np.round(ssr, 4),
                np.round(sst, 4))
    evalDict = {
        'count': count, 'predictionMean': predictionMean, 'yMean': yMean,
        'MAE': mae, 'MAPE': mape, 'MSE': mse, 'R': r, 'R2': r2, 'RMSE': rmse, 'SSE': sse, 'SSR': ssr, 'SST': sst
    }

    print(text)
    return text, evalDict


def randColor():
    colors = ['#DC143C', '#DB7093', '#FF1493', '#4B0082', '#0000FF', '#0000FF', '#000080', '#778899', '#4682B4',
              '#00BFFF', '#5F9EA0', '#FFFF00', '#FFA500', '#DEB887', '#FF7F50', '#FF6347']
    return colors[random.randint(0, len(colors) - 1)]


def plot_and_save(x, y, title, x_label, y_label):
    """
    绘制图像后，保存数据文件
    :param x:
    :param y:
    :param title:
    :param x_label:
    :param y_label:
    :return:
    """
    plt.plot(x, y, color='#8FBC8F', linestyle='dashed', label='label')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()
    f = open('evaluation.txt', mode='a')
    # 格式  x::y::title::x_label::y_label
    f.write('{}::{}::{}::{}::{}\n'.format(','.join(map(str, x)), ','.join(map(str, y)), title, x_label, y_label))
    f.close()


def parse():
    """
    解析分析结果文件
    :return:
    """
    evalName = 'MSE Fit'  # 指标名称
    f = open('../evaluation.txt', mode='r')
    file_data = f.read()
    f.close()
    lines = file_data.splitlines()
    curves = []
    for line in lines:
        x, y, title, x_label, y_label = line.split("::")
        x, y = list(map(float, x.split(","))), list(map(float, y.split(",")))  # 解析出来的每一个元素都是str类型，转化为int或float类型
        curves.append({
            'x': x, 'y': y, 'title': title, 'x_label': x_label, 'y_label': y_label
        })

    for curve in curves:
        x, y, title, x_label, y_label = curve['x'], curve['y'], curve['title'], curve['x_label'], curve['y_label']
        title = title[0:title.find("(")]
        plt.plot(x, y, color=randColor(), linestyle='dashed', label=title)

    plt.xlabel(curves[0]['x_label'])
    plt.ylabel(curves[0]['y_label'])
    plt.title('{} for some techniques'.format(evalName))
    plt.legend()
    plt.show()

# parse()
