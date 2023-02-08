import warnings

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QComboBox, \
    QListWidget, QListWidgetItem, QGridLayout, QCheckBox, QScrollArea, QFileDialog
import pyqtgraph as pg
import time
from threading import Timer

import dataprocess.loss_eval as loss_eval
from techniques.interface import AbstractTechnique


class DataModifyWindow(QWidget):
    # 曲线widget双击鼠标后弹出
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, x, y, parent):
        super().__init__()
        self.x, self.y = x, y
        self.text = ''
        self.plotDataItem = None
        self.parent = parent
        self.setWindowTitle("标记管理")
        commentLayout = QHBoxLayout()  # 文字
        self.commentLabel = QLabel("添加注释")
        self.commetText = QLineEdit()
        self.commetText.textChanged.connect(self.onTextChanged)

        self.commentWipe = QPushButton("擦除")  # 擦除
        self.commentWipe.clicked.connect(self.onWipeComment)
        commentLayout.addWidget(self.commentLabel)
        commentLayout.addWidget(self.commetText)
        commentLayout.addWidget(self.commentWipe)

        layout = QVBoxLayout()
        xLayout = QHBoxLayout()
        yLayout = QHBoxLayout()

        layout.addLayout(commentLayout)
        layout.addLayout(xLayout)
        layout.addLayout(yLayout)

        self.xLabel, self.yLabel = QLabel('X:'), QLabel('Y:')
        self.xText, self.yText = QLineEdit('{}'.format(self.x)), QLineEdit('{}'.format(self.y))

        xLayout.addWidget(self.xLabel)
        xLayout.addWidget(self.xText)

        yLayout.addWidget(self.yLabel)
        yLayout.addWidget(self.yText)

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        self.confirmBtn = QPushButton("确认")
        self.cancelBtn = QPushButton("取消")

        self.confirmBtn.clicked.connect(self.onConfirm)
        self.cancelBtn.clicked.connect(self.onCancel)

        buttonLayout.addWidget(self.confirmBtn)
        buttonLayout.addWidget(self.cancelBtn)

        self.setLayout(layout)
        self.show()

    def onConfirm(self, evt):
        if self.text is None or len(self.text) == 0:
            # 没有标记数据，则清除plotWidget中的数据点并删除parent对其的引用
            self.close()
            del self.parent.dataModifyWindow[(self.x, self.y)]
            self.parent.technique.plotWidget.removeItem(self.plotDataItem)
            return
        x, y = [], []
        x.append(self.x)
        y.append(self.y)
        if self.plotDataItem is not None:
            # plotDataItem对象存在，不论有没有修改text，都重新绘制
            self.parent.technique.plotWidget.removeItem(self.plotDataItem)
        pen = pg.mkPen(color=(255, 0, 0), width=30)
        self.plotDataItem = self.parent.technique.plotWidget.plot(x, y, pen=pen, name=self.text)
        self.plotDataItem.setSymbol('x')
        self.plotDataItem.setSymbolSize(15)
        self.plotDataItem.sigClicked.connect(self.onItemClicked)
        self.hide()

    def onTextChanged(self, s):
        self.text = s

    def onCancel(self):
        self.hide()

    def onWipeComment(self):
        self.commetText.clear()

    def onItemClicked(self, item):
        self.show()


class ErrorInfoWidget(QWidget):
    # 错误提示窗口
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        picLabel = QLabel()
        picLabel.setPixmap(QPixmap('icons/error.svg'))
        picLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label = QLabel(objectName="ErrInfo")

        button = QPushButton("确认")
        button.clicked.connect(self.onClick)
        layout.addWidget(picLabel)
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setLayout(layout)
        self.setWindowTitle("Error")

    def showInfo(self, info: str):
        self.label.setText(info)
        self.show()

    def onClick(self):
        self.close()


class DerivativeWidget(QWidget):
    """
    k阶导数
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('导数')

        self.currentIndex = 0  # 阶数
        self.lsqPoints = 7  # 最小二乘点数

        listWidget = QListWidget()
        items = []
        for i in range(1, 5):
            items.append('{}rd Order Derivative'.format(i))
        listWidget.addItems(items)
        listWidget.currentTextChanged.connect(self.onTextChanged)

        lsqLabel = QLabel('最小二乘点数：')

        lsqBox = QComboBox()  # 最小二乘拟合点数选择
        lsqBox.addItems([str(i) for i in range(5, 50) if i % 2 != 0])
        lsqBox.currentTextChanged.connect(self.onLsqChanged)
        lsqBox.setCurrentText('7')

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        layout = QHBoxLayout()
        layout.addWidget(listWidget)
        layout.addWidget(lsqLabel)
        layout.addWidget(lsqBox)
        layout.addWidget(button)
        self.setLayout(layout)

    def onClick(self):
        self.parent.technique.n_derivative(self.currentIndex, self.lsqPoints)
        self.close()

    def onLsqChanged(self, s):
        self.lsqPoints = int(s)

    def onTextChanged(self, s):
        self.currentIndex = int(s[0])


class SmoothWidget(QWidget):
    # 数据平滑
    def __init__(self, parent):
        super().__init__()
        self.points = 5  # 平滑窗口数
        self.polyorder = 3  # 阶数
        self.choose = 'S-G平滑'  # 平滑方式选择
        self.showLossEval = False

        self.parent = parent
        self.setWindowTitle('平滑')
        layout = QGridLayout()
        chooseLabel = QLabel('方式选择:')  # 平滑方式选择文字提示
        chooseList = QListWidget()
        chooseList.addItems(['S-G平滑', '傅里叶变换平滑'])
        chooseList.currentTextChanged.connect(self.onChoose)

        pointsLabel = QLabel('平滑窗口点数:')  # window length选择 在5-49的奇数
        pointsBox = QComboBox()
        pointsBox.addItems([str(i) for i in range(5, 50) if i % 2 != 0])
        pointsBox.currentTextChanged.connect(self.onPoints)

        polyorderLabel = QLabel('阶数:')
        polyorderBox = QComboBox()
        polyorderBox.addItems([str(i) for i in range(2, 10)])
        polyorderBox.currentTextChanged.connect(self.onPolyorder)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        evalAllBtn = QPushButton('整体平滑效果')
        evalAllBtn.clicked.connect(self.onEvalAll)

        # 误差评估
        lossEvalBox = QCheckBox('拟合评估结果')
        self.showLossEval = False
        lossEvalBox.stateChanged.connect(self.onLossEvalState)

        layout.addWidget(chooseLabel, 0, 0)
        layout.addWidget(chooseList, 0, 1)
        layout.addWidget(pointsLabel, 1, 0)
        layout.addWidget(pointsBox, 1, 1)
        layout.addWidget(polyorderLabel, 2, 0)
        layout.addWidget(polyorderBox, 2, 1)
        layout.addWidget(button, 3, 0)
        layout.addWidget(evalAllBtn, 3, 1)
        layout.addWidget(lossEvalBox, 4, 0)

        self.setLayout(layout)

    def onClick(self):
        self.close()
        if self.points <= self.polyorder:
            self.parent.errInfoWidget.showInfo(
                'polyorder({}) must be less than window_length({})!'.format(self.points, self.polyorder))
            return
        techniqueName, dataDict = self.parent.technique.smooth(self.points, self.polyorder, self.choose)
        if self.showLossEval:
            evalResult, _ = self.parent.technique.lossEval(techniqueName,
                                                           'Savitzky-Golay smooth. points={}, polyorder={}'.format(
                                                               self.points, self.polyorder))
            self.parent.popoutRef = LossReportWidget(evalResult)
            self.parent.popoutRef.show()

    def onEvalAll(self):
        self.close()
        technique = self.parent.technique
        title, xLabel, yLabel = '{} S-G Smooth'.format(technique.techniqueName), 'points', 'R-Square'
        points, polyorder = [5, 9, 15, 21, 27, 33, 41, 49], 3
        x, y = [], []
        for point in points:
            techniqueName, dataDict = technique.smooth(point, polyorder, '')
            _, evalDict = technique.lossEval(techniqueName,
                                             '() Savitzky-Golay smooth. points={}, polyorder={}'.format(
                                                 technique.techniqueName, point, polyorder))
            x.append(point)
            y.append(evalDict['R2'])

        loss_eval.plot_and_save(x, y, title, xLabel, yLabel)

    def onLossEvalState(self, state):
        self.showLossEval = state == Qt.Checked

    def onChoose(self, s):
        # 平滑方法选择
        self.choose = s

    def onPoints(self, s):
        # window length 选择
        self.points = int(s)

    def onPolyorder(self, s):
        self.polyorder = int(s)


class IntegrateWidget(QWidget):
    """
    积分，提供复合梯形积分和复合辛普森积分
    """

    def __init__(self, parent):
        super(IntegrateWidget, self).__init__()
        self.nameDict = {
            '复合梯形': 'trapezoid', '复合辛普森': 'simpson'
        }
        self.parent = parent
        self.setWindowTitle('积分')
        self.name = 'trapezoid'  # 积分方式，默认复合梯形
        layout = QHBoxLayout()
        self.setLayout(layout)

        chooseLabel = QLabel('积分规则选择')
        chooseList = QListWidget()
        chooseList.addItems(['复合梯形', '复合辛普森'])
        chooseList.currentTextChanged.connect(self.onChoose)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        layout.addWidget(chooseLabel)
        layout.addWidget(chooseList)
        layout.addWidget(button)

    def onClick(self):
        self.parent.technique.integrate(self.nameDict[self.name])
        self.close()

    def onChoose(self, s: str):
        # print('integrate name:', s)
        self.name = s


class InterpolateWidget(QWidget):
    """
    插值，b-spline插值
    """

    def __init__(self, parent):
        super(InterpolateWidget, self).__init__()
        self.parent = parent
        self.setWindowTitle('插值')
        self.density = 2  # 插入数据点密度
        layout = QHBoxLayout()

        chooseLabel = QLabel('数据插入密度(density)')
        chooseBox = QComboBox()
        chooseBox.addItems(['x2', 'x4', 'x8', 'x16', 'x32', 'x64'])
        chooseBox.currentTextChanged.connect(self.onChoose)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        layout.addWidget(chooseLabel)
        layout.addWidget(chooseBox)
        layout.addWidget(button)
        self.setLayout(layout)

    def onClick(self):
        self.parent.technique.interpolate(self.density)
        self.close()

    def onChoose(self, s):
        print('density:', s[1:])
        self.density = int(s[1:])


class BaselineFitWidget(QWidget):
    def __init__(self, parent):
        super(BaselineFitWidget, self).__init__()
        self.deg = 1  # 对于多项式最小二乘算法，默认阶数是1
        self.algorithm = '普通最小二乘'  # 默认算法，普通最小二乘
        self.setWindowTitle("基线拟合与扣除")
        self.confirm = '无操作'  # 确认时操作
        self.parent = parent

        self.fromPeak, self.toPeak = 0, 0
        self.peaks = []
        self.clipMode = 'linear'

        mainLayout = QGridLayout()

        # 峰底两侧 子layout
        mainLayout.addWidget(QLabel("峰底两侧", objectName='Title1'), 0, 0)
        mainLayout.addWidget(self.addPeakWidget(), 1, 0)
        peaksWidget = QWidget()
        self.peaksLayout = QVBoxLayout()
        peaksWidget.setLayout(self.peaksLayout)
        mainLayout.addWidget(peaksWidget, 2, 0)

        # 基线拟合算法 子layout
        mainLayout.addWidget(QLabel('基线拟合算法', objectName='Title1'), 3, 0)

        fitWidget = QWidget()
        fitLayout = QGridLayout()
        fitWidget.setLayout(fitLayout)
        # 选择拟合算法
        fitLayout.addWidget(QLabel('算法选择: '), 0, 0)
        algWidget = QComboBox()
        algWidget.currentTextChanged.connect(self.onAlgChoose)
        algWidget.addItems(['最小二乘', '正则化最小二乘'])
        fitLayout.addWidget(algWidget, 0, 1)
        # 基线拟合项次 选择
        fitLayout.addWidget(QLabel('基线拟合项次'), 1, 0)
        degWidget = QComboBox()
        degWidget.addItems([str(i) for i in range(1, 15)])
        degWidget.currentTextChanged.connect(self.onDegChoose)
        fitLayout.addWidget(degWidget, 1, 1)
        # 削峰方式
        fitLayout.addWidget(QLabel('削峰方式'), 2, 0)
        clipBox = QComboBox()
        clipBox.addItems(['linear', 'max', 'min'])
        clipBox.currentTextChanged.connect(self.onClip)
        fitLayout.addWidget(clipBox, 2, 1)
        mainLayout.addWidget(fitWidget, 4, 0)

        # 确认时操作
        mainLayout.addWidget(QLabel('确认时操作', objectName='Title1'), 5, 0)
        confirmWidget = QWidget()
        confirmLayout = QHBoxLayout()
        confirmWidget.setLayout(confirmLayout)
        cfmBox = QComboBox()  # 选择确认时操作
        cfmBox.addItems(['无操作', '差值', '基线'])
        cfmBox.currentTextChanged.connect(self.onConfirm)
        confirmLayout.addWidget(cfmBox)
        mainLayout.addWidget(confirmWidget, 6, 0)

        # 确认按钮
        button = QPushButton('确认')
        button.clicked.connect(self.onClick)
        mainLayout.addWidget(button, 0, 1)
        # 新增峰两侧按钮
        addPeakButton = QPushButton('新增峰两侧')
        mainLayout.addWidget(addPeakButton, 1, 1)
        addPeakButton.clicked.connect(self.onAddPeak)
        # 整体拟合效果评估，并画出拟合图像
        evalAllButton = QPushButton('整体拟合效果评估')
        evalAllButton.clicked.connect(self.onEvalAll)
        mainLayout.addWidget(evalAllButton, 2, 1)

        # 误差评估
        lossEvalBox = QCheckBox('拟合评估结果')
        self.showLossEval = False
        lossEvalBox.stateChanged.connect(self.onLossEvalState)
        mainLayout.addWidget(lossEvalBox, 7, 0)

        self.setLayout(mainLayout)

    def onEvalAll(self):
        self.close()
        technique = self.parent.technique
        key, xLabel, yLabel = 'MSE', 'Degree of Polynomial', 'Mean Squared Error'
        title = '{} baseline fit (1-14 degree)'.format(technique.techniqueName)
        x, y = [], []
        for deg in range(1, 15):
            techniqueName, dataDict = technique.baseline_fit(deg, '最小二乘', False, self.peaks, self.clipMode)
            evalResult, evalDict = technique.lossEval(techniqueName, '{} baseline fit({} degree)'.format(technique.techniqueName, deg))
            x.append(deg)
            y.append(evalDict[key])
        loss_eval.plot_and_save(x, y, title, xLabel, yLabel)

    def onClick(self):
        techniqueName, dataDict = self.parent.technique.baseline_fit(self.deg, self.algorithm, self.confirm == '差值', self.peaks, self.clipMode)

        self.hide()
        if self.showLossEval:
            evalResult, _ = self.parent.technique.lossEval(techniqueName, '{} baseline fit({} degree)'.format(
                self.parent.technique.techniqueName, self.deg))
            self.parent.popoutRef = LossReportWidget(evalResult)
            self.parent.popoutRef.show()

    def addPeakWidget(self):
        # 产生峰值范围选择的widget, number为编号
        widget = QWidget(self)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('from'))
        fromEdit = QLineEdit()
        layout.addWidget(fromEdit)
        layout.addWidget(QLabel('to'))
        toEdit = QLineEdit()
        layout.addWidget(toEdit)
        widget.setLayout(layout)

        fromEdit.textChanged.connect(self.onFromPeak)
        toEdit.textChanged.connect(self.onToPeak)
        return widget

    def onAddPeak(self):
        if self.fromPeak-self.toPeak == 0:
            return
        label = QLabel('Peak{}: from {} to {}'.format(len(self.peaks), self.fromPeak, self.toPeak))
        self.peaksLayout.addWidget(label)
        self.peaks.append((self.fromPeak, self.toPeak))

    def onFromPeak(self, s):
        if len(s) == 1 and s == '-': return
        self.fromPeak = float(s) if len(s) != 0 else 0

    def onToPeak(self, s):
        if len(s) == 1 and s == '-': return
        self.toPeak = float(s) if len(s) != 0 else 0

    def onClip(self, s):
        self.clipMode = s

    def onLossEvalState(self, state):
        self.showLossEval = state == Qt.Checked

    def onAlgChoose(self, s: str):
        # 选择算法
        self.algorithm = s

    def onDegChoose(self, s):
        # 多项式最小二乘阶数
        self.deg = int(s)

    def onConfirm(self, s):
        self.confirm = s


class FourierSpectrumWidget(QWidget):
    """
    傅里叶频谱
    """

    def __init__(self, parent):
        super(FourierSpectrumWidget, self).__init__()
        self.setWindowTitle('fourier spectrum')
        self.parent = parent
        self.xScale, self.yScale, self.yExpres = '1/sec(Hz)', 'linear', 'magnitude'

        mainLayout = QGridLayout()

        xScaleLabel = QLabel("X Scale")
        mainLayout.addWidget(xScaleLabel, 0, 0)

        xScaleList = QListWidget()
        xScaleList.addItems(['nth component', '1/sec(Hz)', '1/V'])
        xScaleList.currentTextChanged.connect(self.onXScaleList)
        mainLayout.addWidget(xScaleList, 1, 0)

        yScaleLabel = QLabel('Y Scale')
        mainLayout.addWidget(yScaleLabel, 0, 1)

        yScaleList = QListWidget()
        yScaleList.addItems(['linear', 'logrithmic'])
        yScaleList.currentTextChanged.connect(self.onYScaleList)
        mainLayout.addWidget(yScaleList, 1, 1)

        yExpreLabel = QLabel('Y Expression')
        mainLayout.addWidget(yExpreLabel, 2, 0)

        yExpreList = QListWidget()
        yExpreList.addItems(['magnitude', 'real', 'imag'])
        yExpreList.currentTextChanged.connect(self.onYExpreList)
        mainLayout.addWidget(yExpreList, 3, 0)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)
        mainLayout.addWidget(button, 0, 3)

        self.setLayout(mainLayout)

    def onClick(self):
        self.parent.technique.fft(self.xScale, self.yScale, self.yExpres)
        self.close()

    def onXScaleList(self, s):
        self.xScale = s

    def onYScaleList(self, s):
        self.yScale = s

    def onYExpreList(self, s):
        self.yExpres = s


class BackgroundSubtractionWidget(QWidget):
    """
    背景扣除
    """

    def __init__(self, parent):
        super(BackgroundSubtractionWidget, self).__init__()
        self.parent = parent
        self.setWindowTitle('背景扣除')
        self.file_path, self.file_type = None, None

        self.showLossEval = False  # 是否显示误差评估结果

        mainLayout = QGridLayout()
        openFileBtn = QPushButton('选择文件')
        openFileBtn.clicked.connect(self.onOpenFile)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        self.pathLabel = QLabel()

        showLossEvalBox = QCheckBox('误差评估')
        showLossEvalBox.stateChanged.connect(self.onCheck)

        mainLayout.addWidget(openFileBtn, 0, 0)
        mainLayout.addWidget(button, 0, 1)
        mainLayout.addWidget(self.pathLabel, 1, 0)
        mainLayout.addWidget(showLossEvalBox, 2, 0)

        self.setLayout(mainLayout)

    def onCheck(self, state):
        self.showLossEval = state

    def onOpenFile(self):
        self.file_path, self.file_type = QFileDialog.getOpenFileName(self, "选取目录", "./", "Files (*.txt *.bin)")
        if self.file_path is None or len(self.file_path) == 0:
            warnings.warn('error on open file.')
        self.pathLabel.setText(self.file_path)

    def onClick(self):
        if self.file_path is None or len(self.file_path) == 0:
            self.parent.errInfoWidget.showInfo('尚未选择文件')
            return
        technique, file_data = self.parent.parseFile(self.file_path, self.file_type)
        x, y = technique.curX, technique.curY
        file_name = technique.file_name.split("/")[-1]
        self.parent.technique.background_subtraction(x, y, file_name)
        if self.showLossEval == Qt.Checked:
            self.parent.popoutRef = LossReportWidget(loss_eval.evaluate(self.parent.technique.curY, y))
            self.parent.popoutRef.show()
        self.close()


class LossReportWidget(QWidget):
    def __init__(self, text):
        super(LossReportWidget, self).__init__()
        self.setWindowTitle('误差评估结果')

        mainLayout = QHBoxLayout()
        widget = QLabel(text, objectName='Style1')
        mainLayout.addWidget(widget)
        self.setLayout(mainLayout)


class GraphicOptionWidget(QWidget):
    """
    图形选项弹出窗口
    """

    def __init__(self, parent, basicParams, additionalParams, mainPlots):
        super(GraphicOptionWidget, self).__init__()
        self.parent = parent
        self.setWindowTitle("图形选项")
        mainLayout = QGridLayout()

        # 屏幕列
        label = QLabel('屏幕：', objectName='Title1')
        mainLayout.addWidget(label, 0, 0)

        mainLayout.addWidget(self.pattern1('标题(&E)', self.onBaseline), 1, 0)
        mainLayout.addWidget(self.pattern1('轴(&X)', self.onBaseline), 2, 0)
        mainLayout.addWidget(self.pattern1('基线(&B)', self.onBaseline), 3, 0)
        mainLayout.addWidget(self.pattern1('参数(&M)', self.onParams), 4, 0)
        mainLayout.addWidget(self.pattern1('结果(&R)', self.onResult), 5, 0)

        # 打印机列
        label = QLabel('打印机：', objectName='Title1')
        mainLayout.addWidget(label, 0, 1)

        mainLayout.addWidget(self.pattern1('标题(&E)', self.onResult), 1, 1)
        mainLayout.addWidget(self.pattern1('轴(&X)', self.onResult), 2, 1)
        mainLayout.addWidget(self.pattern1('基线(&B)', self.onResult), 3, 1)
        mainLayout.addWidget(self.pattern1('参数(&M)', self.onResult), 4, 1)
        mainLayout.addWidget(self.pattern1('结果(&R)', self.onResult), 5, 1)

        # 网络与反转列
        label = QLabel('网络与反转：', objectName='Title1')
        mainLayout.addWidget(label, 0, 2)

        mainLayout.addWidget(self.pattern1('X轴网格', self.onResult), 1, 2)
        mainLayout.addWidget(self.pattern1('Y轴网格', self.onResult), 2, 2)
        mainLayout.addWidget(self.pattern1('X轴反转', self.onResult), 3, 2)
        mainLayout.addWidget(self.pattern1('Y轴反转', self.onResult), 4, 2)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)
        mainLayout.addWidget(button, 0, 4)

        # x轴冻结
        mainLayout.addWidget(self.pattern2('x轴冻结', '-0.1', '至', '0.5'), 6, 0, 1, 4)

        # y轴冻结
        mainLayout.addWidget(self.pattern2('y轴冻结', '2e6', '至', '1.4e-5'), 7, 0, 1, 4)

        # x轴标题
        mainLayout.addWidget(self.pattern2('x轴标题', '', '单', ''), 8, 0, 1, 4)
        # y轴标题
        mainLayout.addWidget(self.pattern2('y轴标题', '', '单', ''), 9, 0, 1, 4)

        self.setLayout(mainLayout)

    def pattern1(self, text, func):
        widget = QCheckBox(text)
        widget.stateChanged.connect(func)
        return widget

    def pattern2(self, topic, text1, text2, text3):
        """
        布局模板
        :return:
        """
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        checkBox = QCheckBox(topic)
        fromEdit = QLineEdit(text1)
        label = QLabel(text2)
        toEdit = QLineEdit(text3)
        layout.addWidget(checkBox)
        layout.addWidget(fromEdit)
        layout.addWidget(label)
        layout.addWidget(toEdit)
        return widget

    def onClick(self):
        self.close()

    def onBaseline(self, state):  # 基线
        pass

    def onParams(self, state):  # 参数
        pass

    def onResult(self, state):  # 结果
        pass


class DataListWidget(QWidget):
    """
    数据列表
    """

    def __init__(self, parent):
        super(DataListWidget, self).__init__()
        self.parent = parent
        self.setWindowTitle('数据列表')

        textEdit = QLabel(self.parent.file_data)
        textEdit.resize(600, 900)
        scroll = QScrollArea()
        scroll.setWidget(textEdit)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        layout = QHBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(button)
        self.setLayout(layout)

    def onClick(self):
        self.close()


class DataInfoWidget(QWidget):
    def __init__(self, parent):
        super(DataInfoWidget, self).__init__()
        self.parent = parent
        mainLayout = QGridLayout()
        self.setWindowTitle("数据信息")

        content = "文件名: {}\n源: {}\n型号: {}\n日期: {}\nROM Vers: {}\nProg: {}\n" \
            .format(self.parent.technique.basicParams['File'].split("/")[-1],
                    self.parent.technique.basicParams['Data Source'],
                    self.parent.technique.basicParams['Instrument Model'],
                    self.parent.technique.basicParams['Date'], '', '')
        widget = QLabel(content, objectName="Style1")
        mainLayout.addWidget(widget, 0, 0)

        mainLayout.addWidget(QLabel('--------------------------'), 1, 0)

        widget = QLabel("数据处理执行:", objectName="Title1")
        widget.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(widget, 2, 0)

        processContent = ['Smoothing', '1st Derivative', '2nt Derivative', '3nt Derivative', '4nt Derivative',
                          'Integration', 'Semi-Derivative', 'Semi-Integral', 'Interpolation', 'BaseLine Correlation',
                          'Data Point Removing', 'Data Point Modifying', 'Background Substraction', 'Signal Avg',
                          'X math', 'Y math']
        listWidget = QListWidget()
        listWidget.addItems(processContent)
        mainLayout.addWidget(listWidget, 2, 1)

        mainLayout.addWidget(QLabel("标题: ", objectName="Style1"), 3, 0)
        mainLayout.addWidget(QLabel("注: ", objectName="Style1"), 4, 0)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)
        mainLayout.addWidget(button, 0, 3)

        self.setLayout(mainLayout)

    def onClick(self):
        self.close()


class ClockWidget(QWidget):
    def __init__(self, parent):
        super(ClockWidget, self).__init__()
        self.parent = parent
        mainLayout = QHBoxLayout()
        self.setWindowTitle("时间")

        self.label = QLabel(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), objectName="Style1")
        mainLayout.addWidget(self.label)

        self.setLayout(mainLayout)
        self.task()

    def task(self):
        self.label.setText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        Timer(1, self.task, ()).start()


class PersistCurveWidget(QWidget):
    """
    持久化曲线数据
    """

    def __init__(self, parent):
        super(PersistCurveWidget, self).__init__()
        self.setWindowTitle("持久化曲线")
        self.parent = parent
        self.techniqueDict = self.parent.technique.childTechniqueDict
        mainLayout = QGridLayout()

        infoLabel = QLabel('曲线选择')

        curveBox = QComboBox()
        self.curveName = ''
        curveBox.addItems(list(self.techniqueDict.keys()))
        curveBox.currentTextChanged.connect(self.onTextChanged)

        button = QPushButton('确认')
        button.clicked.connect(self.onClick)

        mainLayout.addWidget(infoLabel, 0, 0)
        mainLayout.addWidget(curveBox, 1, 0)
        mainLayout.addWidget(button, 0, 1)
        self.setLayout(mainLayout)

    def onClick(self):
        if self.curveName not in self.techniqueDict:
            self.parent.technique.errInfoWidget.showInfo('无此曲线')
            self.close()
            return
        hint = ''
        if 'Data Proc' in self.techniqueDict[self.curveName].basicParams:
            hint = self.techniqueDict[self.curveName].basicParams['Data Proc'] + " unnamed"
        filePath, fileType = QFileDialog.getSaveFileName(self, '保存路径', "./{}".format(hint),
                                                         "text (*.txt);;binary (*.bin)")
        self.techniqueDict[self.curveName].persist(filePath)
        self.close()

    def onTextChanged(self, s):
        self.curveName = s
