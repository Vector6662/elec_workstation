from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit
import pyqtgraph as pg


class DataModifyWindow(QWidget):
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
        plotData = self.parent.acv.plotWidget.plot(x, y, pen=pen)
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


class ErrorOnNewLab(QWidget):
    # 点击”开始实验“后，跳出此窗口，表示提示需要打开com端口接收数据
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        picLabel = QLabel()
        picLabel.setPixmap(QPixmap('icons/error.svg'))
        picLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label = QLabel("can not open com port!", objectName="ErrInfo")

        button = QPushButton("确认")
        button.clicked.connect(self.onClick)
        layout.addWidget(picLabel)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
        self.setWindowTitle("Error")
        self.show()

    def onClick(self):
        self.close()
