from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QComboBox, \
    QListWidget, QListWidgetItem, QGridLayout, QCheckBox
import pyqtgraph as pg


class DataModifyWindow(QWidget):
    # 曲线widget双击鼠标后弹出
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, x, y, parent):
        super().__init__()
        self.x, self.y = x, y
        self.parent = parent
        self.setWindowTitle("修改数据点")
        commentLayout = QHBoxLayout()  # 文字
        self.commentLabel = QLabel("添加注释")
        self.commetText = QLineEdit()
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

        self.xLabel, self.yLabel = QLabel('x(A):'), QLabel('y(V):')
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

    def showData(self, x, y):
        self.x, self.y = x, y
        self.xText.setText('{}'.format(self.x))
        self.yText.setText('{}'.format(self.y))
        self.show()

    def onConfirm(self, evt):
        print(self.xText.text(), self.yText.text())
        x, y = [], []
        x.append(self.x)
        y.append(self.y)
        pen = pg.mkPen(color=(255, 0, 0), width=30)
        plotData = self.parent.technique.plotWidget.plot(x, y, pen=pen)
        plotData.setSymbol('x')
        plotData.setSymbolSize(15)
        plotData.sigClicked.connect(self.onHover)
        self.hide()

    def onCancel(self):
        self.hide()

    def onWipeComment(self):
        self.commetText.clear()

    def onHover(self, ev):
        print(ev)


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
        self.currentIndex = 0
        self.listWidget = QListWidget()
        items = []
        for i in range(1, 5):
            items.append('{}rd Order Derivative'.format(i))

        self.listWidget.addItems(items)
        self.listWidget.currentTextChanged.connect(self.onTextChanged)
        button = QPushButton('确认')
        button.clicked.connect(self.onClick)
        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(button)
        self.setLayout(layout)

    def onClick(self):
        self.parent.technique.n_derivative(deg=self.currentIndex)
        self.close()

    def onTextChanged(self, s):
        self.currentIndex = int(s[0])


class SmoothWidget(QWidget):
    # 数据平滑
    def __init__(self, parent):
        super().__init__()
        self.points = 5  # 平滑窗口数
        self.polyorder = 3  # 阶数
        self.choose = 'S-G平滑'  # 平滑方式选择

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

        layout.addWidget(chooseLabel, 0, 0)
        layout.addWidget(chooseList, 0, 1)
        layout.addWidget(pointsLabel, 1, 0)
        layout.addWidget(pointsBox, 1, 1)
        layout.addWidget(polyorderLabel, 2, 0)
        layout.addWidget(polyorderBox, 2, 1)
        layout.addWidget(button, 3, 0)

        self.setLayout(layout)

    def onClick(self):
        # print('points', self.points, 'way', self.choose)
        if self.points <= self.polyorder:
            self.parent.errInfoWidget.showInfo(
                'polyorder({}) must be less than window_length({})!'.format(self.points, self.polyorder))
            return

        self.parent.technique.smooth(self.points, self.polyorder, self.choose)
        self.close()

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
        mainLayout = QGridLayout()

        # 峰底两侧 子layout
        mainLayout.addWidget(QLabel("峰底两侧", objectName='Title1'), 0, 0)
        peeksWidget = QWidget()
        self.peeksLayout = QVBoxLayout()
        peeksWidget.setLayout(self.peeksLayout)
        self.peekWidgetList = []  # 添加的peekWidget
        self.peekWidgetList.append(self.addPeekWidget(0))
        self.peeksLayout.addWidget(self.peekWidgetList[0])
        mainLayout.addWidget(peeksWidget, 1, 0)

        # 新增峰两侧按钮
        addPeekButton = QPushButton('新增')
        mainLayout.addWidget(addPeekButton, 2, 0)
        addPeekButton.clicked.connect(self.onAddPeek)

        # 基线拟合算法 子layout
        mainLayout.addWidget(QLabel('基线拟合算法', objectName='Title1'), 3, 0)

        fitWidget = QWidget()
        fitLayout = QGridLayout()
        fitWidget.setLayout(fitLayout)
        fitLayout.addWidget(QLabel('算法选择: '), 0, 0)
        algWidget = QComboBox()  # 选择拟合算法
        algWidget.currentTextChanged.connect(self.onAlgChoose)
        algWidget.addItems(['最小二乘', '正则化最小二乘'])
        fitLayout.addWidget(algWidget, 0, 1)
        fitLayout.addWidget(QLabel('基线拟合项次'), 1, 0)
        degWidget = QComboBox()  # 基线拟合项次 选择
        degWidget.addItems([str(i) for i in range(1, 15)])
        degWidget.currentTextChanged.connect(self.onDegChoose)
        fitLayout.addWidget(degWidget, 1, 1)
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

        self.setLayout(mainLayout)

    def addPeekWidget(self, number: int):
        # 产生峰值范围选择的widget, number为编号
        widget = QWidget(self)
        widget.setStatusTip(str(number))
        layout = QHBoxLayout()
        layout.addWidget(QLabel('from'))
        fromEdit = QLineEdit()
        layout.addWidget(fromEdit)
        layout.addWidget(QLabel('to'))
        toEdit = QLineEdit()
        layout.addWidget(toEdit)
        widget.setLayout(layout)
        return widget

    def onClick(self):
        difference = False
        if self.confirm == '差值':
            difference = True
        self.parent.technique.baseline_fit(self.deg, self.algorithm, difference)
        self.close()

    def onAddPeek(self):
        widget = self.addPeekWidget(len(self.peekWidgetList))
        self.peekWidgetList.append(widget)
        self.peeksLayout.addWidget(widget)

    def onAlgChoose(self, s: str):
        # 选择算法
        self.algorithm = s

    def onDegChoose(self, s):
        # 多项式最小二乘阶数
        self.deg = int(s)

    def onConfirm(self, s):
        self.confirm = s
