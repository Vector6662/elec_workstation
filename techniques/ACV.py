import math
import time

import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QLabel
import numpy as np


class ACV:
    def __init__(self, parent, file_name, file_type):
        if len(file_name) == 0:
            return
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
        for i in range(19, self.num):
            item = lines[i].split(",")
            x.append(round(float(item[0]), 4))
            y.append(round(float(item[1]) * math.pow(10, self.Sensitivity), 4))

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
        self.plotWidget = pg.PlotWidget()
        self.posWidget = QLabel()
        self.textWidget = QLabel()

        # self.plotItem.addItem(self.textItem)
        # self.plotItem.addItem(self.posItem)
        # self.graphicWidget.addItem(self.textItem, 0, 1)
        # self.graphicWidget.addItem(self.plotWidget, 1, 0)
        # self.graphicWidget.addItem(self.posItem, 2, 0)

        self.textWidget.setText(text)
        self.textWidget.setFixedSize(300, 700)

        pen = pg.mkPen(color=(255, 0, 0), width=3)
        styles = {'color': 'green', 'font-size': '30px', 'font-weight': '900'}
        self.plotWidget.setLabel('left', "AC Current/1e-{}A".format(self.Sensitivity), **styles)
        self.plotWidget.setLabel('bottom', "Potential/V", **styles)
        self.plotWidget.setBackground("w")

        self.plotWidget.showGrid(x=True, y=True)
        self.plotWidget.plot(x, y, pen=pen)





