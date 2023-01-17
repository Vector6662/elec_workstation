import string
import math

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QComboBox, \
    QListWidget, QListWidgetItem, QGridLayout, QCheckBox
import techniques.dataprocess as dp


def open_file(file_name):
    if file_name is None or len(file_name) == 0:
        TypeError('error on open file.')
        return
    with open(file_name, "r") as f:  # 返回文件对象
        data = f.read()
    f.close()
    return data.splitlines()


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
        self.sensitivity, self.symbol = None, None  # 灵敏度，符号，正或负
        self.analyseParams = {}  # 分析参数
        # 数据
        self.dataDict = {}
        self.curX, self.curY, self.curXLabel, self.curYLabel = None, None, None, None
        labelStartIndex = self.parseParams()  # 模板方法，解析以上属性
        self.parseData(labelStartIndex)
        # 各个部件
        self.parameterWidget = self.initParameterWidget()
        self.plotWidget, self.mainPlotData = self.initPlotWidget()
        # 展示坐标
        self.positionWidget = QLabel()

    def parseParams(self) -> int:
        """
        解析数据过程，需要子类重写。需要解析以下属性
        additionalParams字典，即每种测试技术特定的参数
        symbol，sensitivity绝对值
        analyseParams：分析参数字典，也是每种测试技术特定参数
        :return: label start index. label在文件行中的地址
        """
        pass

    def parseData(self, start):
        labels = self.lines[start].split(",")
        labelIndex = {}  # 记录每一个label在lines中的索引，从0开始
        idx = 0
        for label in labels:
            self.dataDict[label] = []
            labelIndex[idx] = label
            idx = idx + 1
        length = idx  # label总数，也即len(labels)
        for i in range(start + 2, len(self.lines)):
            item = self.lines[i].split(",")
            for j in range(length):  # 解析每一行的各列
                s = item[j]
                if "e" in s:
                    val = round(float(s) * math.pow(10, self.sensitivity), 4)
                else:
                    val = round(float(s), 4)
                self.dataDict[labelIndex[j]].append(val)
        self.curX, self.curY = self.dataDict[labels[0]], self.dataDict[labels[1]]
        self.curXLabel, self.curYLabel = labels[0], labels[1] + "(1e{}{})".format(self.symbol, self.sensitivity)

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
        layout.addWidget(QLabel(basicText, objectName='BasicParams'))
        layout.addWidget(QLabel(additionalText, objectName='BasicParams'))
        layout.addWidget(QLabel(analysisText, objectName='AdditionalParams'))

        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedSize(300, 700)

        return widget

    def initPlotWidget(self):
        """
        需要子类重写
        解析并返回实验曲线
        :return:
        """
        plotWidget = pg.PlotWidget()  # 曲线展示
        pen = pg.mkPen(color=(255, 0, 0), width=3)
        styles = {'color': 'green', 'font-size': '30px', 'font-weight': '900'}
        plotWidget.setLabel('left', self.curYLabel, **styles)
        plotWidget.setLabel('bottom', self.curXLabel, **styles)
        plotWidget.setBackground("w")
        plotWidget.addLegend()

        plotWidget.showGrid(x=True, y=True)
        mainPlotData = plotWidget.plot(self.curX, self.curY, pen=pen, name='当前波形')  # 绘制主曲线
        mainPlotData.setSymbolSize(8)
        return plotWidget, mainPlotData  # 组件和主曲线

    def showDataPoint(self, flag: bool):
        # 显示/隐藏原始数据点
        if flag:
            self.mainPlotData.setSymbol('o')
        else:
            self.mainPlotData.setSymbol(None)

    def getCur(self) -> (string, list, string, list):
        """
        可能需要重写
        当前label以及数据
        :return:
        """

    def smooth(self, window_length, polyorder, name):
        x, y = self.curX, dp.smooth(self.curX, self.curY, window_length, polyorder)
        self.plotWidget.plot(x, y, name=name, pen=pg.mkPen(width=2, color=(1, 2, 3)))

    def n_derivative(self, deg: int):
        x, y = self.curX, dp.n_derivative(self.curX, self.curY, deg)
        self.plotWidget.plot(x, y, name='{}rd Order Derivative'.format(deg), pen=pg.mkPen(width=2))

    def integrate(self, name: str):
        if name == 'trapezoid':
            x, y = self.curX, dp.integrate_trapezoid(self.curX, self.curY)
        elif name == 'simpson':
            x, y = self.curX, dp.integrate_simpson(self.curY, self.curY)
        else:
            raise ValueError("no such integrate type. should be trapezoid or simpson.")
        self.plotWidget.plot(x, y, name=name, pen=pg.mkPen(width=2, cosmetic=True))

    def interpolate(self, density: int):
        x, y = dp.interpolate(self.curX, self.curY, density)
        self.plotWidget.plot(x, y, name='B-Spline插值', pen=pg.mkPen(width=2))

    def baseline_fit(self, deg, algorithm, difference: bool):
        """

        :param deg: 拟合阶数
        :param algorithm: 拟合算法
        :param difference: 显示差值与否
        :return:
        """
        if algorithm == '普通最小二乘':
            x, y = dp.lsq_fit(self.curX, self.curY, deg)
        elif algorithm == '多项式最小二乘':
            x, y = dp.ols_fit(self.curX, self.curY)
        else:
            raise ValueError("不存在此类拟合算法")
        if difference:
            # todo 显示与原数据之差
            pass
        self.plotWidget.plot(x, y, name=algorithm + '({}阶)'.format(deg), pen=pg.mkPen(width=2, color=(100, 0, 0)))
