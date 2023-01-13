import math
import time

import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QLabel
import numpy as np
import techniques.dataprocess as dp
from gui.another_window import DerivativeWidget


class AbstractTechnique:
    def __init__(self, parent, file_name, file_type):
        if file_name is None or len(file_name) == 0:
            TypeError('error when open file.')
            return
        with open(file_name, "r") as f:  # 返回文件对象
            data = f.read()
        f.close()
        lines = data.splitlines()
        technique = lines[1]  # 测试技术


class ACV:
    def __init__(self, parent, file_name, file_type):
        if len(file_name) == 0:
            return
        self.parent = parent
        # open()会自动返回一个文件对象
        f = open(file_name, "r")  # 打开路径所对应的文件， "r"以只读的方式 也是默认的方式
        with f:
            data = f.read()
        f.close()
        lines = data.splitlines()
        self.num = len(lines)

        date = lines[0]
        technique = lines[1]
        file = "{} ({})".format(file_name.split("/")[-1], file_name)
        DataSource = lines[3].split(":")[1]
        InstrumentModel = lines[4].split(":")[1]

        InitE = float(lines[8].split("=")[1])
        FinlaE = float(lines[9].split("=")[1])
        IncrE = float(lines[10].split("=")[1])
        Amplitude = float(lines[11].split("=")[1])
        Frequency = float(lines[12].split("=")[1])
        SamplePeriod = float(lines[13].split("=")[1])
        QuietTime = float(lines[14].split("=")[1])
        sen = lines[15].split("=")[1]
        self.Sensitivity = int(lines[15].split("=")[1].replace("1e-", ""))

        x, y = [], []
        self.xToy = {}
        for i in range(19, self.num):
            item = lines[i].split(",")
            curX, curY = round(float(item[0]), 4), round(float(item[1]) * math.pow(10, self.Sensitivity), 4)
            self.xToy[curX] = curY
            x.append(curX)
            y.append(curY)
        self.x, self.y = x, y

        imax = max(y)

        ep, ip, ap = 0, 0, 0

        text = "{}\nTech:ACV\nFile:{}\n\n" \
               "Init E(V) = {}\nFinal E(V) = {}\nIncr E(V) = {}\nAmplitude(V) = {}\n" \
               "Frequency (Hz) = {}\nSample Period (sec) = {}\nQuiet Time (sec) = {}\nSensitivity(A/V) = {}\n\n" \
               "Ep = {}V\nip = {}A\nAp = {}VA" \
            .format(date, file, InitE, FinlaE, IncrE, Amplitude, Frequency, SamplePeriod, QuietTime, sen,
                    ep, ip, ap)

        # widgets
        # 如果后续代码有问题，考虑构造器传入parent参数
        self.plotWidget = pg.PlotWidget()  # 曲线展示
        self.textWidget = QLabel()  # 曲线信息。实验参数显示
        self.posWidget = QLabel()  # 展示坐标

        self.textWidget.setText(text)
        self.textWidget.setFixedSize(300, 700)

        pen = pg.mkPen(color=(255, 0, 0), width=3)
        styles = {'color': 'green', 'font-size': '30px', 'font-weight': '900'}
        self.plotWidget.setLabel('left', "AC Current/1e-{}A".format(self.Sensitivity), **styles)
        self.plotWidget.setLabel('bottom', "Potential/V", **styles)
        self.plotWidget.setBackground("w")
        self.plotWidget.addLegend()

        self.plotWidget.showGrid(x=True, y=True)
        self.mainPlotData = self.plotWidget.plot(x, y, pen=pen, name='当前波形')  # 绘制主曲线
        self.mainPlotData.setSymbolSize(8)

        # blue_pen = pg.mkPen(color='b', width=2)
        # p_x, p_y = fit(x, y)
        # self.plotWidget.plot(p_x, p_y, pen=new_pen)
        # self.plotWidget.plot(x, dp.integrate(x, y), pen=blue_pen)

        # gree_pen = pg.mkPen(color='g', width=2)
        # x_interp, y_interp = dp.interpolate(x, y, 2)
        # self.plotWidget.plot(x_interp, y_interp, pen=gree_pen)

    def showDataPoint(self, flag: bool):
        # 显示/隐藏原始数据点
        if flag:
            self.mainPlotData.setSymbol('o')
        else:
            self.mainPlotData.setSymbol(None)

    def smooth(self, window_length, polyorder, name):
        x, y = self.x, dp.smooth(self.x, self.y, window_length, polyorder)
        self.plotWidget.plot(x, y, name=name, pen=pg.mkPen(width=2, color=(1, 2, 3)))

    def n_derivative(self, deg: int):
        x, y = self.x, dp.n_derivative(self.x, self.y, deg)
        self.plotWidget.plot(x, y, name='{}rd Order Derivative'.format(deg), pen=pg.mkPen(width=2))

    def integrate(self, name: str):
        if name == 'trapezoid':
            x, y = self.x, dp.integrate_trapezoid(self.x, self.y)
        elif name == 'simpson':
            x, y = self.x, dp.integrate_simpson(self.x, self.y)
        else:
            raise ValueError("no such integrate type. should be trapezoid or simpson.")
        self.plotWidget.plot(x, y, name=name, pen=pg.mkPen(width=2, cosmetic=True))

    def interpolate(self, density: int):
        x, y = dp.interpolate(self.x, self.y, density)
        self.plotWidget.plot(x, y, name='B-Spline插值', pen=pg.mkPen(width=2))

    def baseline_fit(self, deg, algorithm, difference: bool):
        """

        :param deg: 拟合阶数
        :param algorithm: 拟合算法
        :param difference: 显示差值与否
        :return:
        """
        if algorithm == '普通最小二乘':
            x, y = dp.lsq_fit(self.x, self.y, deg)
        elif algorithm == '多项式最小二乘':
            x, y = dp.ols_fit(self.x, self.y)
        else:
            raise ValueError("不存在此类拟合算法")
        if difference:
            # todo 显示与原数据之差
            pass
        self.plotWidget.plot(x, y, name=algorithm + '({}阶)'.format(deg), pen=pg.mkPen(width=2, color=(100, 0, 0)))

