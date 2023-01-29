import random
import string
import math

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QComboBox, \
    QListWidget, QListWidgetItem, QGridLayout, QCheckBox
import techniques.dataprocess as dp
from uitls import randomColor


class AbstractTechnique:
    def __init__(self, parent, lines, file_name, file_type):
        self.lines = lines
        # 解析基础参数
        self.basicParams = {
            'date': self.lines[0],
            'techniqueName': self.lines[1],  # 测试技术名称
            'file': "{} ({})".format(file_name.split("/")[-1], file_name),
            'dataSource': self.lines[3].split(":")[1],
            'instrumentModel': self.lines[4].split(":")[1],
            'header': self.lines[5].split(":")[1],
            'note': self.lines[6].split(":")[1]
        }
        # 各测试技术实验附加参数、分析参数
        self.additionalParams = {}  # 附加参数
        self.analyseParams = {}  # 分析参数
        # 数据
        self.carryDict = {}  # 每一个label的进位
        self.dataDict = {}
        # 当前曲线信息
        self.curX, self.curY, self.curXLabel, self.curYLabel = None, None, None, None
        self.curXCarry, self.curYCarry = None, None
        self.xKey, self.xUnit, self.yKey, self.yUnit = None, None, None, None  # 坐标实时显示是的信息。如t=1.23s,Q=2.34e-1C
        self.curves = []

        # 以下是模板方法，解析以上属性，均可重写
        labelStartIndex = self.parseParams()
        self.parseData(labelStartIndex)
        self.parseAnalyseParams()
        self.parseCurrentCurves()

        # 初始化主界面各个部件
        self.parameterWidget = self.initParameterWidget()
        self.plotWidget, self.mainPlots = self.initPlotWidget()
        # 展示坐标
        self.positionWidget = QLabel(objectName='Position')

    def parseParams(self) -> int:
        """
        解析数据过程，需要子类重写。需要解析以下属性
        additionalParams字典，即每种测试技术特定的参数
        analyseParams：分析参数字典，也是每种测试技术特定参数。有些测试技术（如acv）此过程的解析依赖所有数据，因此在此之后需要在完成parseAnalyseParams方法的重写
        :return: label start index. label在文件行中的地址
        """
        pass

    def parseData(self, start):
        labels = []
        for label in self.lines[start].split(","):  # 去掉字符串前后的空格
            labels.append(label.strip())

        self.carryDict = {}  # 每一列数据的进位，格式为："Potential/V":-6
        indexToLabel = {}  # 记录每一个label在lines中的索引，从0开始。格式为1:"Current/A"
        idx = 0
        for label in labels:
            self.dataDict[label] = []
            self.carryDict[label] = -1000  # 初始化为最小值
            indexToLabel[idx] = label
            idx = idx + 1
        length = idx  # label总数，也即len(labels)
        # 获得每一列的进位，为科学计数法的最大值
        for i in range(start + 2, len(self.lines)):
            item = self.lines[i].split(",")
            for j in range(length):  # 解析每一行的各列
                s, label = item[j], indexToLabel[j]
                # 两种情况，如果数据字符串中有字符'e'，表明此列数据是采用的科学计数法，否则为普通数值
                if "e" in s:
                    carry = int(s.split("e")[1])
                    self.carryDict[label] = max(self.carryDict[label], carry)
                else:
                    self.carryDict[label] = 0
        # 存储数据，以label为key
        for i in range(start + 2, len(self.lines)):
            item = self.lines[i].split(",")
            for j in range(length):
                s, label = item[j], indexToLabel[j]
                carry = self.carryDict[label]
                if "e" in s:
                    str1, str2 = s.split("e")[0], s.split("e")[1]
                    val = float(str1) * math.pow(10, int(str2) - carry)
                else:
                    val = float(s)
                self.dataDict[label].append(round(val, 4))

    def parseCurrentCurves(self):
        """
        解析当前曲线数据，需要解析
        curX, curY,
        curXLabel, curYLabel
        curXCarry，curYCarry：当前数据的进位
        self.xKey, self.xUnit, self.yKey, self.yUnit
        curves
        可重写。部分测试技术label显示文字会有不同
        注意，curves[0]必须为所有数据连续的曲线
        :return:

        """
    def parseAnalyseParams(self):
        """
        可选，解析分析参数。大部分测试技术此部分的解析在parseParams中就能完成
        如acv，分析参数的解析依赖数据所有数据，于是在parseParams后设置此步骤以解析此类数据
        :return:
        """
        pass

    def formatParameterTexts(self):
        """
        根据不同测试技术，可重写，这里给出的是通用的解析方式
        :return:
        """
        basicText = "{}\nTech: {}\nFile: {}".format(self.basicParams['date'], self.basicParams['techniqueName'],
                                                    self.basicParams['file'])
        additionalText = ""
        for key in self.additionalParams:
            additionalText += "{} = {}\n".format(key, self.additionalParams[key])

        analysisText = ""
        for key in self.analyseParams:
            analysisText += "{} = {}\n".format(key, self.analyseParams[key])
        return basicText, additionalText, analysisText

    def initParameterWidget(self) -> QWidget:
        # 初始化主界面右侧参数展示部件，初始化布局
        basicText, additionalText, analysisText = self.formatParameterTexts()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.addWidget(QLabel(basicText, objectName='BasicParams'))
        layout.addWidget(QLabel(additionalText, objectName='BasicParams'))
        layout.addWidget(QLabel(analysisText, objectName='AdditionalParams'))

        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedSize(400, 700)

        return widget

    def initPlotWidget(self):
        """
        需要子类重写
        解析并返回实验曲线
        :return:
        """
        plotWidget = pg.PlotWidget()  # 曲线展示
        styles = {'color': 'green', 'font-size': '30px', 'font-weight': '900'}
        plotWidget.setLabel('left', self.curYLabel, **styles)
        plotWidget.setLabel('bottom', self.curXLabel, **styles)
        plotWidget.setBackground("w")
        plotWidget.addLegend()

        plotWidget.showGrid(x=True, y=True)
        plots = []
        for i in range(0, len(self.curves)):
            if i == 0 and len(self.curves) > 1:  # 若有切分的segment，则不显示i=0的曲线，即主曲线
                continue
            pen = pg.mkPen(color=randomColor(), width=3)
            x, y = self.curves[i]['x'], self.curves[i]['y']
            plot = plotWidget.plot(x, y, pen=pen, name='segment {}'.format(i))
            plot.setSymbolSize(8)
            plots.append(plot)
        return plotWidget, plots  # 组件和曲线对象

    def showPoints(self, flag: bool):
        # 显示/隐藏原始数据点
        for plot in self.mainPlots:
            plot.setSymbol('o') if flag else plot.setSymbol(None)

    def getCur(self) -> (string, list, string, list):
        """
        可能需要重写
        当前label以及数据
        :return:
        """

    def smooth(self, window_length, polyorder, name):
        pen = pg.mkPen(width=2, color=randomColor())
        curve = self.curves[0]
        x, y = curve['x'], dp.smooth(curve['x'], curve['y'], window_length, polyorder)
        self.plotWidget.plot(x, y, name="{} of main curve".format(name), pen=pen)

    def n_derivative(self, deg: int):
        pen = pg.mkPen(width=2, color=randomColor())
        curve = self.curves[0]
        x, y = curve['x'], dp.n_derivative(curve['x'], curve['y'], deg)
        self.plotWidget.plot(x, y, name='{}rd Order Derivative of main curve'.format(deg), pen=pen)

    def integrate(self, name: str):
        pen = pg.mkPen(width=2, color=randomColor(), cosmetic=True)
        curve = self.curves[0]
        x, y = curve['x'], dp.integrate_trapezoid(curve['x'], curve['y']) \
            if name == 'trapezoid' else dp.integrate_simpson(curve['x'], curve['y'])
        self.plotWidget.plot(x, y, name="{} of main curve".format(name), pen=pen)

    def interpolate(self, density: int):
        pen = pg.mkPen(width=2, color=randomColor())
        curve = self.curves[0]
        x, y = curve['x'], dp.interpolate(curve['x'], curve['y'], density)
        self.plotWidget.plot(x, y, name='B-Spline interpolate of main curve', pen=pen)

    def baseline_fit(self, deg, algorithm, difference: bool):
        """

        :param deg: 拟合阶数
        :param algorithm: 拟合算法
        :param difference: 显示差值与否
        :return:
        """
        pen = pg.mkPen(width=2, color=randomColor())
        curve = self.curves[0]
        if algorithm == '最小二乘':
            x, y = dp.lsq_fit(curve['x'], curve['y'], deg)
        elif algorithm == '正则化最小二乘':
            x, y = dp.ols_fit(curve['x'], curve['y'], deg)
        else:
            raise ValueError("不存在此类拟合算法")
        if difference:
            # todo 显示与原数据之差
            pass
        self.plotWidget.plot(x, y, name="{}({}阶) of main curve".format(algorithm, deg), pen=pen)
