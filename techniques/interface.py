import math
import random
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from pyqtgraph import ScatterPlotItem

import dataprocess.loss_eval as loss_eval
import techniques.dataprocess as dp
from uitls import randomColor, parseBasicParamsHelper, parseCurveHelper, formatBasicParamsHelper


def randColor():
    colors = ['#DC143C', '#DB7093', '#FF1493', '#4B0082', '#0000FF', '#0000FF', '#000080', '#778899', '#4682B4',
              '#00BFFF', '#5F9EA0', '#FFFF00', '#FFA500', '#DEB887', '#FF7F50', '#FF6347']
    return colors[random.randint(0, len(colors) - 1)]


class AbstractTechnique:
    def __init__(self, parent, lines, file_name, file_type):
        """

        :param parent:
        :param lines: 为None或''时创建一个空对象
        :param file_name:
        :param file_type:
        """
        if lines is None or len(lines) == 0:  # 此参数传空用来构造一个空对象
            return
        self.lines, self.file_name, self.file_type = lines, file_name, file_type
        self.techniqueName = self.file_name.split('/')[-1].split('.')[0] + '(main curve)'
        # 解析参数
        self.basicParams = {}  # 基础参数
        self.additionalParams = {}  # 附加参数
        # 数据
        self.carryDict = {}  # 每一个label的进位
        self.dataDict = {}
        # 当前曲线信息
        self.curX, self.curY, self.curXLabel, self.curYLabel = None, None, None, None
        self.curXCarry, self.curYCarry = None, None
        self.curXLabelAlias, self.curYLabelAlias = None, None  # 别名，用于坐标轴上显示标签
        self.curves = []
        # 解析出的数据封装成technique对象，用于持久化等操作
        self.childTechniqueDict = {}

        # 坐标实时显示是的信息。如t=1.23s,Q=2.34e-1C
        self.xKey, self.xUnit, self.yKey, self.yUnit = None, None, None, None

        # 以下是模板方法，解析以上属性，均可重写
        labelStartIndex = self.parseParams()
        # 解析采集数据和曲线
        self.parseData(labelStartIndex)
        self.parseCurrentCurves()

        # 初始化主界面各个部件
        self.parameterWidget = self.initParameterWidget()
        self.plotWidget, self.mainPlots = self.initPlotWidget()

        # self.mark_peaks()  # 自动峰值检测
        # 展示坐标
        self.positionWidget = QLabel(objectName='Position')

        self.peak_indices = None  # 峰值索引列表
        self.peaksScatterItem = None  # 峰值标记plot

    def parseParams(self) -> int:
        """
        解析数据过程，需要子类重写。需要解析以下属性
        additionalParams字典，即每种测试技术特定的参数
        :return: label start index. label在文件行中的地址
        """
        self.basicParams, start = parseBasicParamsHelper(self.lines, self.file_name)
        # 解析附加参数
        for i in range(start, len(self.lines)):
            line = self.lines[i]
            if len(line) == 0:
                continue
            if "/" in line and "," in line:
                start = i
                break
            split = re.split(r'[:=]', line)
            k, v = split[0].strip(), split[1].strip()
            self.additionalParams[k] = v
        return start

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
                # 这里似乎并不需要保留4位小数，因为数据文件中每一个数据本来就只保留了4位
                self.dataDict[label].append(val)

        # 加上高斯白噪
        # i = 0
        # for label in self.dataDict:
        #     if i == 0:
        #         i += 1
        #         continue
        #     self.dataDict[label] += dp.wgn(self.dataDict[label], 30)

    def parseCurrentCurves(self):
        """
        确定x、y数据的label，以及坐标显示数据的key和单位
        可重写。部分测试技术坐标轴上显示可能不同显示文字会有不同
        注意，curves[0]必须为所有数据连续的曲线
        :return:

        """
        self.defaultCurveParser()

    def defaultCurveParser(self, cur_x_label=None, cur_y_label=None, x_key='X', x_unit='', y_key='Y', y_unit='',
                           x_label_alias=None, y_label_alias=None):
        """
        提供主曲线默认解析方案。记录主曲线（curves属性，索引0），记录本对象（childTechniqueDict，索引0）
        :return: 
        """
        # 如果没有指定cur_x_label或cur_y_label，默认为第0、1个数据项的label
        self.curXLabel, self.curYLabel = \
            list(self.dataDict.keys())[0] if cur_x_label is None else cur_x_label, \
            list(self.dataDict.keys())[1] if cur_y_label is None else cur_y_label

        self.curX, self.curY, self.curXCarry, self.curYCarry, self.curXLabelAlias, self.curYLabelAlias \
            = parseCurveHelper(self.dataDict, self.carryDict, self.curXLabel, self.curYLabel, x_label_alias,
                               y_label_alias)
        self.xKey, self.xUnit, self.yKey, self.yUnit = x_key, x_unit, y_key, y_unit
        # 主曲线默认索引为0
        self.curves.append({'x': self.curX, 'y': self.curY})
        # 数据处理时产生的曲线，以AbstractTechnique对象存储，方便后续持久化。初始化为类自己
        self.childTechniqueDict[self.techniqueName] = self

    def formatParameterTexts(self):
        """
        根据不同测试技术，可重写，这里给出的是通用的解析方式
        :return:
        """
        basicText = formatBasicParamsHelper(self.basicParams)
        additionalText = ""
        for key in self.additionalParams:
            additionalText += "{} = {}\n".format(key, self.additionalParams[key]) if len(self.additionalParams[key]) != 0 else '{}\n'.format(key)
        return basicText, additionalText

    def initParameterWidget(self) -> QWidget:
        # 初始化主界面右侧参数展示部件，初始化布局
        basicText, additionalText = self.formatParameterTexts()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.addWidget(QLabel(basicText, objectName='BasicParams'))
        layout.addWidget(QLabel(additionalText, objectName='AdditionalParams'))

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
        plotWidget.setLabel('bottom', self.curXLabelAlias, **styles)
        plotWidget.setLabel('left', self.curYLabelAlias, **styles)
        plotWidget.setBackground("w")
        plotWidget.addLegend()

        plotWidget.showGrid(x=True, y=True)
        plots = []
        for i in range(0, len(self.curves)):
            if i == 0 and len(self.curves) > 1:  # 若有切分的segment，则不显示i=0的曲线，即主曲线
                continue
            pen = pg.mkPen(color=randomColor(), width=3)
            x, y = self.curves[i]['x'], self.curves[i]['y']
            plot = plotWidget.plot(x, y, pen=pen, name='segment {} of {}'.format(i, self.techniqueName))
            plot.setSymbolSize(8)
            plots.append(plot)
        return plotWidget, plots  # 组件和曲线对象

    def showPoints(self, flag: bool):
        # 显示/隐藏原始数据点
        for plot in self.mainPlots:
            plot.setSymbol('o') if flag else plot.setSymbol(None)

    def plot_graph(self):
        import matplotlib.pyplot as plt
        title, xlabel, ylabel = '', 'Frequency/Hz', 'log(FT Coefficient)'
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        x, y = self.dataDict[self.curXLabel], self.dataDict[self.curYLabel]
        plt.plot(x, y)
        plt.show()

    def wrap(self, data_dict: dict, data_proc_name=None):
        """
        封装一个当前类的深拷贝，并封装新数据。适用于持久化数据处理结果之前的操作
        :return:
        """
        # 尝试使用深拷贝，但对象中有QWidget类型的实例，应该是不能被拷贝的，有报错：TypeError: cannot pickle 'QWidget' object
        # import copy
        # technique = copy.deepcopy(self)
        # 拷贝
        technique = AbstractTechnique(None, None, None, None)
        technique.basicParams = self.basicParams.copy()
        technique.additionalParams = self.additionalParams.copy()

        if data_proc_name is not None:
            del technique.basicParams['Header']
            del technique.basicParams['Note']
            technique.basicParams['Data Proc'] = data_proc_name
            technique.basicParams['Header'], technique.basicParams['Note'] = \
                self.basicParams['Header'], self.basicParams['Note']
        # 各数据项进位
        technique.carryDict = self.carryDict.copy()
        # 各数据项数据处理,加上进位
        technique.dataDict = {}
        for label in list(data_dict.keys()):
            technique.dataDict[label] = data_dict[label]
        return technique

    def persist(self, file_path: str):
        lines, index = [], 0
        # 基础参数
        for key in self.basicParams:
            v = self.basicParams[key]
            lines.append(v + '\n' if key == 'Date' or key == 'TechniqueName' else "{}: {}\n".format(key, v))
        lines.append('\n')
        # 附加参数
        for key in self.additionalParams:
            v = self.additionalParams[key]
            lines.append("{} = {}\n".format(key, v))
        lines.append('\n')
        # 数据列表项。在此之前对每一列数据加上进位
        dataDict = self.dataDict.copy()
        labels = list(dataDict.keys())
        for label in labels:
            carry, data = self.carryDict[label], dataDict[label]
            # 加上进位，精度控制在三位小数
            dataDict[label] = np.round(np.round(data, 3) * np.power(10.0, carry), abs(carry) + 3)

        lines.append(', '.join(labels) + '\n')
        lines.append('\n')
        # 数据列
        for i in range(len(dataDict[labels[0]])):
            item = []
            for key in dataDict.keys():
                item.append(str(dataDict[key][i]))
            lines.append(', '.join(item) + '\n')
        # 写入文件
        f = None
        try:
            f = open(file_path, 'w')
            f.writelines(lines)
        except:
            warnings.warn('写入文件失败')
            return
        finally:
            if f:
                f.close()

    def lossEval(self, technique_name, title=None):
        """
        误差评估
        :param title:
        :param technique_name:
        :return: 格式化的误差评估结果
        """
        actualName, predictName = list(self.childTechniqueDict.keys())[0], technique_name
        actualTechnique, predictTechnique = self.childTechniqueDict[actualName], self.childTechniqueDict[predictName]
        label = self.curYLabel
        actualY, predictY = actualTechnique.dataDict[label], predictTechnique.dataDict[label]
        return loss_eval.evaluate(actualY, predictY, actualName, predictName, title)

    def smooth(self, window_length, polyorder, name):
        dataDict = self.dataDict.copy()
        labels = list(self.dataDict.keys())
        xLabel, yLabel = self.curXLabel, self.curYLabel
        x = self.dataDict[xLabel]
        for label in labels:
            if label == xLabel:
                continue
            y = dp.smooth(x, dataDict[label], window_length, polyorder)
            dataDict[label] = y
        techniqueName = 'S-G smooth of main curve(window_length={}, polyorder={})'.format(window_length, polyorder)
        self.childTechniqueDict[techniqueName] = self.wrap(dataDict, 'Smooth')
        self.plotWidget.plot(x, dataDict[yLabel], name=techniqueName, pen=pg.mkPen(width=2, color=randomColor()))
        return techniqueName, dataDict

    def n_derivative(self, deg: int, lsq_points: int):
        # 首先完成lsq平滑
        # _, dataDict = self.smooth(lsq_points, 3, '')
        # dataDict = dataDict.copy()

        dataDict = self.dataDict.copy()
        # 进行n阶导数
        labels = list(dataDict.keys())
        xLabel, yLabel = self.curXLabel, self.curYLabel
        x = dataDict[xLabel]
        for label in labels:
            if label == xLabel:
                continue
            y = dp.n_derivative(x, dataDict[label], deg)
            dataDict[label] = y
        techniqueName = '{}th Order Derivative of main curve. lsq points={}'.format(deg, lsq_points)
        self.childTechniqueDict[techniqueName] = self.wrap(dataDict, "Derivative")
        self.plotWidget.plot(x, dataDict[yLabel], name=techniqueName, pen=pg.mkPen(width=2, color=randomColor()))
        return techniqueName, dataDict

    def integrate(self, name: str):
        import dataprocess.integrate as integrate
        dataDict = self.dataDict.copy()
        labels = list(dataDict.keys())
        xLabel, yLabel = self.curXLabel, self.curYLabel
        x = dataDict[xLabel]
        for label in labels:
            if label == xLabel:
                continue
            y = integrate.integrate_cumulative(dataDict[label], x, name)
            dataDict[label] = y
        curY = dataDict[yLabel]
        techniqueName = 'integrate({}) of main curve'.format(name)
        self.childTechniqueDict[techniqueName] = self.wrap(dataDict, "Integrate")
        self.plotWidget.plot(x, curY, name=techniqueName, pen=pg.mkPen(width=2, color=randomColor(), cosmetic=True))
        return techniqueName, dataDict

    def interpolate(self, density: int):
        import dataprocess.bezier as bezier
        dataDict = self.dataDict.copy()
        labels = list(dataDict.keys())
        xLabel, yLabel = self.curXLabel, self.curYLabel
        originX, x = dataDict[xLabel], None
        for label in labels:
            if label == xLabel:
                continue
            x, y = bezier.interpolate(originX, dataDict[label], density)
            dataDict[label] = y
        dataDict[xLabel] = x
        y = dataDict[yLabel]
        techniqueName = 'cubic b-spline of main curve(density={})'.format(density)
        self.childTechniqueDict[techniqueName] = self.wrap(dataDict, "Interpolate")
        self.plotWidget.plot(x, y, name=techniqueName, pen=pg.mkPen(width=2, color=randomColor()))

        # 绘制插值图像
        # c1, c2 = randColor(), 'b'
        # plt.plot(self.curX, self.curY, label=self.techniqueName)
        # plt.plot(x, y, label=techniqueName)
        # plt.legend()
        # a = plt.axes([.4, .2, .4, .4])
        # a.plot(self.curX, self.curY, label=self.techniqueName)
        # a.plot(x, y, label=techniqueName)
        # a.set_xlim(0.1, 0.3)
        # a.set_ylim(1.27, 1.36)
        # plt.show()

    def baseline_fit(self, deg, algorithm, difference: bool, peaks=None, clip_mode='linear'):
        """
        对全数据项进行拟合，并生成technique对象
        :param clip_mode: 削峰方式，linear，max，min
        :param peaks:
        :param deg: 拟合阶数
        :param algorithm: 拟合算法
        :param difference: 显示差值与否
        :return:
        """
        # 所有数据项数据处理
        dataDict = self.dataDict.copy()
        labels = list(dataDict.keys())
        xLabel, yLabel = self.curXLabel, self.curYLabel  # 当前的x, y对应Label的名称，用于绘制图像
        x, originY = dataDict[xLabel], dataDict[yLabel]  # x,y 原始数据序列，因为后边可能会进行绘制差值曲线

        # 峰值扣除
        for peak in peaks:
            from_peak, to_peak = peak
            from_peak, to_peak = from_peak if from_peak < to_peak else to_peak, to_peak if from_peak < to_peak else from_peak
            fromIndex, toIndex = -1, -1
            for i in range(len(x)):
                if from_peak <= x[i] <= to_peak and fromIndex == -1:
                    fromIndex = i
                elif from_peak < x[i] < to_peak and fromIndex != -1:
                    toIndex = i
            fromY, toY = originY[fromIndex], originY[toIndex]
            slope = (fromY - toY) / (fromIndex - toIndex)
            t = np.arange(fromIndex, toIndex, 1)
            # 三种削峰的方式，一种用直线填补，或者最大值
            if clip_mode == 'linear':
                f = slope * (t - fromIndex) + fromY
            elif clip_mode == 'max':
                f = [max(fromY, toY) for _ in range(len(t))]
            else:
                f = [min(fromY, toY) for _ in range(len(t))]
            for i in range(len(f)):
                dataDict[yLabel][i + fromIndex] = f[i]
        # 绘制削峰后曲线
        if len(peaks) > 0:
            self.plotWidget.plot(x, dataDict[yLabel], name='peak clipping({})'.format(clip_mode),
                                 pen=pg.mkPen(width=2, color=randomColor()))

        # 拟合
        for label in labels:
            if self.curXLabel == label:
                continue
            y = dataDict[label]  # 当前数据项对应的y列表
            x, y = dp.lsq_fit(x, y, deg) if algorithm == '最小二乘' else dp.ols_fit(x, y, deg)  # 正则化最小二乘
            dataDict[label] = y

        # 封装本次数据处理结果
        techniqueName = "{}({} degree) of main curve".format(algorithm, deg)
        self.childTechniqueDict[techniqueName] = self.wrap(dataDict, 'Baseline Fit')

        # 绘制当前图像
        curveName = 'fit subtraction of main curve({} degree, {})'.format(deg,
                                                                          algorithm) if difference else techniqueName
        curY = dataDict[yLabel]
        curY = np.subtract(originY, curY) if difference else curY
        self.plotWidget.plot(x, curY, name=curveName, pen=pg.mkPen(width=2, color=randomColor()))

        return techniqueName, dataDict

    def background_subtraction(self, technique, file_name, show_bkgrd):
        # todo 校验x和curX是否相同，否 则
        x, y = technique.dataDict[self.curXLabel], technique.dataDict[self.curYLabel]
        subtract_y = np.subtract(self.curY, y)
        self.plotWidget.plot(self.curX, subtract_y, name='background subtraction with {}'.format(file_name),
                             pen=pg.mkPen(width=2, color=randomColor()))
        if show_bkgrd:
            self.plotWidget.plot(x, y, name='background curve: {}'.format(file_name),
                                 pen=pg.mkPen(width=2, color=randomColor()))

    def signal_average(self, techniques: list):
        y_sum = np.zeros(len(self.curY))
        for technique in techniques:
            x, y = technique.dataDict[self.curXLabel], technique.dataDict[self.curYLabel]
            y_sum += y
        y_avg = y_sum / len(techniques) + 1

        self.plotWidget.plot(self.curX, y_avg,
                             name='signal average with {}'.format(', '.join(item.techniqueName for item in techniques)),
                             pen=pg.mkPen(width=2, color=randomColor()))

    def peak_detect(self, state):
        if self.peak_indices is None:
            x, y = np.asarray(self.dataDict[self.curXLabel]), np.asarray(self.dataDict[self.curYLabel])
            self.peak_indices = dp.AMPD(y)
            self.peaksScatterItem = ScatterPlotItem(x[self.peak_indices], y[self.peak_indices], symbol='o',
                                                    pen=pg.mkPen(width=2, color=(255, 0, 0)))
            self.plotWidget.addItem(self.peaksScatterItem)
        if not state:
            self.peaksScatterItem.hide()
        else:
            self.peaksScatterItem.show()

    def fft(self, x_scale, y_scale, y_expression):
        xLabel, yLabel = self.curXLabel, self.curYLabel  # 当前的x, y对应Label的名称，用于绘制图像
        t, x = np.asarray(self.dataDict[xLabel]), np.asarray(self.dataDict[yLabel])
        fft_size = t.size

        sampling_rate = int(1 / abs(t[1] - t[0]))

        # freqs = np.fft.fftfreq(fft_size, sampling_rate)
        freqs = np.linspace(0, sampling_rate, fft_size)

        xs = x[:fft_size]
        xf = np.fft.fft(xs)
        x_abs = np.abs(xf)  # 幅度
        x_real = np.real(xf)  # 实部
        x_imag = np.imag(xf)  # 虚部
        normalized_xf = x_abs/fft_size  # 归一化
        half_t = t[range(fft_size//2)]
        half_normalized_xf = normalized_xf[range(fft_size//2)]
        # xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
        log_xf = 20 * np.log10(x_abs)  # dB功率谱

        left = 'FT coefficient/1e{}'.format(self.carryDict[yLabel])
        bottom = 'FT Component'

        if x_scale != 'nth component':
            freqs = -1 * freqs

        if y_expression == 'magnitude':
            xfp = x_abs
        elif y_expression == 'real':
            left = 'real {}'.format(left)
            xfp = x_real
        else:
            left = 'imag {}'.format(left)
            xfp = x_imag

        if y_scale == 'logarithmic':
            left = 'log({})'.format(left)
            xfp = 20 * np.log10(xfp)

        self.plotWidget.setLabel('bottom', bottom)
        self.plotWidget.setLabel('left', left)
        self.plotWidget.clear()
        self.plotWidget.plot(freqs, xfp/fft_size, name='fourier spectrum of main curve',
                             pen=pg.mkPen(width=2, color=randomColor()))