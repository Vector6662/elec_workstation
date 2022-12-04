from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import (
    QMainWindow, QMenu, QAction, QStatusBar, QMenuBar, QLabel, QVBoxLayout, QStackedLayout,
    QWidget, QMdiArea, QMdiSubWindow, QTextEdit, QFileDialog, QHBoxLayout, QGridLayout, QToolBar
)
from PyQt5.QtGui import QIcon, QColor, QPalette

import PyQt5
import pyqtgraph as pg
import numpy as np

from gui.handlers import open_file
from techniques.ACV import ACV


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initActions()

        self.acv = None
        self.setWindowTitle("Ch660D电化学工作站")
        self.setMinimumSize(1600, 800)
        # toolbar
        toolbar = self.initToolbar()
        # toolbar = ToolBar(self)
        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

        # menubar
        self.setMenuBar(self.initMenu())

        #
        # self.mdiArea = QMdiArea()
        # self.setCentralWidget(self.mdiArea)
        self.setMouseTracking(True)

    def initMenu(self):
        menu = self.menuBar()
        menu = QMenuBar(menu)
        # File
        file_menu = menu.addMenu("&File")

        file_menu.addAction(self.action_openfile)
        file_menu.addAction("cascade")
        file_menu.addAction("tiled")
        # file_menu.triggered.connect(self.file_action)
        file_menu.addSeparator()

        # settings
        settings_menu = menu.addMenu("&Settings")
        settings_menu.addAction(QAction("test 2", self))

        # control
        control_menu = menu.addMenu("&Control")
        control_menu.addAction(QAction("test 3", self))

        # graphic
        graphic_menu = menu.addMenu("&Graphic")
        graphic_menu.addAction(QAction("test", self))

        # data
        data_menu = menu.addMenu("&Data")
        data_menu.addAction(QAction("test", self))

        return menu

    def contextMenuEvent(self, e):
        # 右键
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())  # 传递位置，否则会在屏幕左上角显示，不会跟随鼠标

    # def file_action(self, e):
    #     print(e.text())
    #     if e.text() == "Open":
    #         open_file(self)
    #
    #         # sub = QMdiSubWindow()
    #         # sub.setLayout(layout)
    #         # sub.setWindowTitle(file_name)
    #         # sub.setMinimumSize(1500, 800)
    #         # self.mdiArea.addSubWindow(sub)
    #         # sub.show()
    #         # self.mdiArea.cascadeSubWindows()  # 层叠


    def initActions(self):
        self.action_openfile = QAction(QIcon("icons/opendir.svg"), "open dir", self)
        self.action_openfile.setStatusTip("open folder")
        self.action_openfile.setCheckable(False)
        self.action_openfile.triggered.connect(self.onOpenfile)

    def initToolbar(self):
        # action:open dir/folder
        toolbar = QToolBar()

        # opendir_action = QAction(QIcon("icons/opendir.svg"), "open dir", self)
        # opendir_action.setStatusTip("open folder")
        # opendir_action.setCheckable(False)
        # opendir_action.triggered.connect(self.open_file)
        toolbar.addAction(self.action_openfile)

        toolbar.addSeparator()
        # action: begin
        begin_action = QAction(QIcon("icons/begin.svg"), "begin", self)
        begin_action.setStatusTip("begin")
        toolbar.addAction(begin_action)

        toolbar.addSeparator()

        # action: pause
        pause_action = QAction(QIcon("icons/pause.svg"), "pause", self)
        pause_action.setStatusTip("pause")
        toolbar.addAction(pause_action)
        return toolbar


    def onMouseMoved(self, evt):  # event是window的，而不是widget的，似乎没有widget会有event
        vb = self.acv.plotWidget.getPlotItem().vb
        if vb.mapSceneToView(evt):
            point = vb.mapSceneToView(evt)
            x, y = round(point.x(), 4), round(point.y(), 4)
            self.acv.posWidget.setText("E={}V, i={}e-{}A".format(x, y, self.acv.Sensitivity))
            # print("x={}V, y={}A".format(x, y))

    def onOpenfile(self):
        open_file(self)


#
# class ToolBar(QToolBar):
#     def __init__(self, window, *__args):
#         super().__init__(*__args)
#
#         self.window = window
#
#         # action:open dir/folder
#         opendir_action = QAction(QIcon("icons/opendir.svg"), "open dir", self)
#         opendir_action.setStatusTip("open folder")
#         opendir_action.setCheckable(False)
#         opendir_action.triggered.connect(self.open_file)
#         self.addAction(opendir_action)
#
#         self.addSeparator()
#         # action: begin
#         begin_action = QAction(QIcon("icons/begin.svg"), "begin", self)
#         begin_action.setStatusTip("begin")
#         self.addAction(begin_action)
#
#         self.addSeparator()
#
#         # action: pause
#         pause_action = QAction(QIcon("icons/pause.svg"), "pause", self)
#         pause_action.setStatusTip("pause")
#         self.addAction(pause_action)
#
#     def open_file(self, evt):
#         open_file(self.window, evt)
