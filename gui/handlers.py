from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QWidget, QAction, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox

from techniques.ACV import ACV


# def open_file(window, evt=None):
#     file_name, file_type = QFileDialog.getOpenFileName(window, "选取目录", "./", "Files (*.txt *.bin)")
#     if len(file_name) == 0:
#         return
#
#     window.acv = ACV(window.window, file_name, file_type)
#
#     window.acv.plotWidget.scene().sigMouseMoved.connect(window.onMouseMoved)  # 目前觉得只有window才能够监听鼠标事件
#     window.acv.plotWidget.scene().sigMouseClicked.connect(window.onMouseClicked)
#
#     layout = QGridLayout()
#     rightLayout = QVBoxLayout()  # 主界面右边的
#     rightLayout.addWidget(window.acv.textWidget)
#
#     layout.addLayout(rightLayout, 0, 1)
#     showPointsWidget = QCheckBox("显示数据点")  # 显示数据点
#     rightLayout.addWidget(showPointsWidget)
#     showPointsWidget.stateChanged.connect()
#
#     layout.addWidget(window.acv.plotWidget, 0, 0)
#     layout.addWidget(window.acv.posWidget, 1, 0)
#
#     widget = QWidget()
#     widget.setLayout(layout)
#     window.setCentralWidget(widget)

# def close_file(window, evt=None):
#     widget = window.centralWidget()
#     if widget is None:
#         return
#     widget.close()
