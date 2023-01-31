"""
误差评估
"""
import math

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate(y_actual, y_predicted):
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
    evalDict = {
        'count': count, 'predictionMean': predictionMean, 'yMean': yMean,
        'mae': mae, 'mape': mape, 'mse': mse, 'r': r, 'r2': r2, 'rmse': rmse, 'sse': sse, 'ssr': ssr, 'sst': sst,
    }
    text = ''
    for key in evalDict:
        text += '{} = {}\n'.format(key, evalDict[key])

    print(text)
    return text
