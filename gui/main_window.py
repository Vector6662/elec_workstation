from PyQt5.QtCore import QFile, Qt
from PyQt5.QtWidgets import (
    QMainWindow, QMenu, QAction, QStatusBar, QMenuBar, QLabel, QVBoxLayout, QStackedLayout,
    QWidget, QMdiArea, QMdiSubWindow, QTextEdit, QFileDialog, QHBoxLayout, QGridLayout, QToolBar, QCheckBox,
    QPushButton, QDialog
)
from PyQt5.QtGui import QIcon, QColor, QPalette, QFont

import PyQt5
import pyqtgraph as pg
import numpy as np
from pyqtgraph.GraphicsScene.mouseEvents import MouseClickEvent

import gui.handlers as handlers
from gui.another_window import DataModifyWindow, ErrorOnNewLab
from techniques.ACV import ACV


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.actions = {}
        self.acv = None
        self.plotMark = None  # 显示鼠标所在坐标点
        self.dataModifyWindow = None  # 数据点修改子窗口
        self.initActions()

        self.setWindowTitle("Ch660D电化学工作站")
        self.setMinimumSize(1600, 800)
        # toolbar
        toolbar = self.initToolbar()
        # toolbar = ToolBar(self)
        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

        # menubar
        self.setMenuBar(self.initMenu())

        self.setMouseTracking(True)

        # 初始状态下的widget，点击后打开文件
        self.initWidget()

    def initWidget(self):
        initWidget = QWidget()
        initWidget.setAutoFillBackground(True)
        initLayout = QGridLayout()
        initWidget.setLayout(initLayout)
        # font = QFont("Roman times", 20, QFont.Bold)
        openFileWidget = QPushButton("打开文件", self, objectName="InitButton")
        # openFileWidget.setFont(font)
        openFileWidget.clicked.connect(self.onOpenfile)
        newLabWidget = QPushButton("开始实验", self, objectName="InitButton")
        # newLabWidget.setFont(font)
        newLabWidget.clicked.connect(self.onNew)

        initLayout.addWidget(openFileWidget, 1, 1)
        initLayout.addWidget(newLabWidget, 2, 1)
        initLayout.addWidget(QWidget(), 1, 0)
        initLayout.addWidget(QWidget(), 2, 0)
        initLayout.addWidget(QWidget(), 1, 2)
        initLayout.addWidget(QWidget(), 2, 2)
        self.setCentralWidget(initWidget)

    def initActions(self):
        actions_dict = {
            # icon path, 名称, status tip, is checkable, handler
            'action_new': ['icons/new.svg', "新建", "new", False, self.onNew],
            'action_openfile': ["icons/opendir.svg", "打开", 'open file', False, self.onOpenfile],
            'action_closefile': ['', '关闭', 'close file', False, self.onClosefile],
            'action_savefile': ['icons/save.svg', '另存为', 'save', False, self.onSavefile],
            'action_print': ['icons/print.svg', '打印', "print", False, self.onPrint],
            'action_technique': ['icons/technique.svg', '实验技术', "technique", False, self.onTechnique],
            'action_exp_params': ['icons/experparams.svg', "实验参数", 'experimental params', False, self.onExpParams],
            'action_run_exper': ['icons/run.svg', '运行实验', 'run experiment', False, self.onRunExper],
            'action_stop_exper': ['icons/pause.svg', '暂停/继续', 'stop/continue', True, self.onStopExper],
            'action_terminate_exper': ['icons/pause.svg', '终止实验', 'terminate', False, self.onTerminateExper],
            'action_reverse_scan': ['icons/reversescan.svg', '反向扫描', 'reverse scan', False, self.onReverseScan],
            'action_zero_current': ['icons/zerocurrent.svg', 'Zero Current', 'Zero Current', False, self.onZeroCurrent],
            'action_dp_smooth': ['', '数据平滑', 'Smoothing', False, self.onDataProcess],  # 平滑
            'action_dp_deriv': ['', '导数', 'Derivatives', False, self.onDataProcess],  # 导数
            'action_dp_integrate': ['', '积分', 'Integration', False, self.onDataProcess],  # 积分
            'action_dp_semi': ['', '半微分和半积分', 'Semiinteg and Semideriv', False, self.onDataProcess],  # 半微分和半积分
            'action_dp_interpolate': ['', '插值', 'Interpolation', False, self.onDataProcess],  # 插值
            'action_dp_baseline_fitting': ['', '基线拟合和扣除', 'Baseline Fitting & Subtraction', False,
                                           self.onDataProcess],  # 基线拟合和扣除
            'action_dp_baseline_correction': ['', '线性基线修正', 'Linear Baseline Correction', False,
                                              self.onDataProcess],  # 线性基线修正
            'action_dp_datapoint_remove': ['', '数据点移除', 'Data Point Removing', False, self.onDataProcess],  # 数据点移除
            'action_dp_datapoint_modify': ['', '数据点修改', 'Data Point Modifying', False, self.onDataProcess],
            # 数据点修改
            'action_dp_backgroud_substract': ['', '背景扣除', 'Background Subtraction', False, self.onDataProcess],
            # 背景扣除
            'action_dp_signal_avg': ['', '信号平均', 'Signal Averaging', False, self.onDataProcess],  # 信号平均
            'action_dp_math_ops': ['', '数学运算', 'Mathematical Operation', False, self.onDataProcess],  # 数学运算
            'action_dp_fourier_spectrum': ['', '傅里叶频谱', 'Fourier Spectrum', False, self.onDataProcess],  # 傅里叶频谱

        }
        self.actions = {}
        for key in actions_dict:
            value = actions_dict[key]
            action = QAction(QIcon(value[0]), value[1], self)
            action.setStatusTip(value[2])
            action.setCheckable(value[3])
            action.triggered.connect(value[4])
            self.actions[key] = action

    def initMenu(self):
        menu = self.menuBar()
        menu = QMenuBar(menu)
        # File
        file_menu = menu.addMenu("文件(&F)")

        file_menu.addAction(self.actions['action_openfile'])
        file_menu.addAction(self.actions['action_closefile'])
        file_menu.addSeparator()

        # settings
        settings_menu = menu.addMenu("设置(&S)")
        settings_menu.addAction(self.actions['action_technique'])
        settings_menu.addAction(self.actions['action_exp_params'])

        # control
        control_menu = menu.addMenu("控制(&C)")
        control_menu.addAction(self.actions['action_run_exper'])
        control_menu.addAction(self.actions['action_stop_exper'])
        control_menu.addAction(self.actions['action_terminate_exper'])

        # graphic
        graphic_menu = menu.addMenu("图像(&G)")

        # data
        data_menu = menu.addMenu("数据处理(&D)")
        for action in self.actions:
            if "action_dp" in action:
                data_menu.addAction(self.actions[action])

        # analyse
        analyse_menu = menu.addMenu("分析")

        # simulate
        simulate_menu = menu.addMenu("模拟")

        # view
        view_menu = menu.addMenu("视图(&V)")

        # window
        window_menu = menu.addMenu("窗口(&W)")

        # help
        help_menu = menu.addMenu("帮助(&H)")

        return menu

    def initToolbar(self):
        toolbar = QToolBar()
        toolbar.addAction(self.actions['action_new'])  # 新建
        toolbar.addAction(self.actions['action_openfile'])  # open file
        toolbar.addAction(self.actions['action_savefile'])
        toolbar.addAction(self.actions['action_print'])

        toolbar.addSeparator()
        toolbar.addSeparator()

        toolbar.addAction(self.actions['action_technique'])  # 实验技术
        toolbar.addAction(self.actions['action_exp_params'])  # 实验参数
        toolbar.addSeparator()
        toolbar.addSeparator()

        toolbar.addAction(self.actions['action_run_exper'])  # 运行实验
        toolbar.addAction(self.actions['action_stop_exper'])  # 暂停/继续
        toolbar.addAction(self.actions['action_terminate_exper'])  # 终止实验
        toolbar.addAction(self.actions['action_reverse_scan'])  # 反向扫描
        toolbar.addAction(self.actions['action_zero_current'])  # zero current

        return toolbar

    def onMouseMoved(self, evt):  # event是window的，而不是widget的，似乎没有widget会有event
        # print('onMouseMoved: ', type(evt), evt.x(), evt.y())

        vb = self.acv.plotWidget.getPlotItem().vb
        if vb.mapSceneToView(evt):
            point = vb.mapSceneToView(evt)
            x, y = round(point.x(), 4), round(point.y(), 4)
            self.acv.posWidget.setText("E={}V, i={}e-{}A".format(x, y, self.acv.Sensitivity))
            # print("x={}V, y={}A".format(x, y))
            # if x not in self.acv.xToy:
            #     return
            # markX, markY = [], []
            # markX.append(x)
            # markY.append(self.acv.xToy[x])
            # if self.plotMark is None:  # 标记鼠标在曲线上的位置
            #     self.plotMark = self.acv.plotWidget.plot(markX, markY, symbol='+')
            # else:
            #     self.plotMark.setData(markX, markY, symbol='+')

    def onMouseClicked(self, evt: MouseClickEvent):
        if not evt.double():
            return
        vb = self.acv.plotWidget.getPlotItem().vb
        if vb.mapSceneToView(evt.scenePos()):
            point = vb.mapSceneToView(evt.scenePos())
            x, y = round(point.x(), 4), round(point.y(), 4)
            # print('click:', "x={}V, y={}A".format(x, y))
            if self.dataModifyWindow is None:
                self.dataModifyWindow = DataModifyWindow(x, y, self)
            else:
                self.dataModifyWindow.showData(x, y)
        # print('onMouseClicked: ', type(evt), 'scene pos:', evt.scenePos(), 'pos:', evt.pos())

    def onNew(self):
        # 新建
        self.errOnNewLab = ErrorOnNewLab()

    def onOpenfile(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取目录", "./", "Files (*.txt *.bin)")
        if len(file_name) == 0:
            return

        self.acv = ACV(self, file_name, file_type)

        self.acv.plotWidget.scene().sigMouseMoved.connect(self.onMouseMoved)  # 目前觉得只有window才能够监听鼠标事件
        self.acv.plotWidget.scene().sigMouseClicked.connect(self.onMouseClicked)

        layout = QGridLayout()
        rightLayout = QVBoxLayout()  # 主界面右边的
        rightLayout.addWidget(self.acv.textWidget)

        layout.addLayout(rightLayout, 0, 1)
        showPointsWidget = QCheckBox("显示数据点")  # 显示数据点
        rightLayout.addWidget(showPointsWidget)
        showPointsWidget.stateChanged.connect(self.onStateChanged)

        layout.addWidget(self.acv.plotWidget, 0, 0)
        layout.addWidget(self.acv.posWidget, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # def onFirstClicked(self,evt):
    #     # 打开window后第一次点击widget，打开文件
    #     print(evt)
    def onStateChanged(self, state):
        # 显示/隐藏原始数据点
        if state == 2:  # checked
            self.acv.showDataPoint(True)
        elif state == 0:  # unchecked
            self.acv.showDataPoint(False)

    def onClosefile(self):
        widget = self.centralWidget()
        if widget is None:
            return
        widget.close()
        self.initWidget()

    def onSavefile(self):
        pass

    def onPrint(self):
        pass

    def onTechnique(self):
        # 实验技术
        pass

    def onExpParams(self):
        # 实验参数
        pass

    def onRunExper(self):
        # 运行实验
        pass

    def onStopExper(self):
        # 暂停/继续
        pass

    def onTerminateExper(self):
        # 终止实验
        pass

    def onReverseScan(self):
        # 反向扫描
        pass

    def onZeroCurrent(self):
        # Zero Current
        pass

    def onDataProcess(self, evt):
        # 数据处理模块的handler
        print('data process:', evt)
