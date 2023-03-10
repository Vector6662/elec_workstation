import time
import warnings

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QStatusBar, QMenuBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QToolBar, QPushButton
)
from pyqtgraph.GraphicsScene.mouseEvents import MouseClickEvent

import techniques.implements
import techniques.interface
from gui.another_window import DataModifyWindow, ErrorInfoWidget, DerivativeWidget, SmoothWidget, IntegrateWidget, \
    InterpolateWidget, BaselineFitWidget, DataListWidget, DataInfoWidget, ClockWidget, GraphicOptionWidget, \
    BackgroundSubtractionWidget, PersistCurveWidget, FourierSpectrumWidget, SignalAvgWidget, FFTFilterWidget


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.configFile = 'chi.cfg'  # 配置文件路径
        self.popoutRef = None  # 当前弹出的窗口
        self.errInfoWidget = ErrorInfoWidget()  # 暂时错误信息
        self.technique = None
        self.dataModifyWindow = {}  # 数据点修改子窗口

        self.setWindowTitle("电化学测试分析软件")
        self.resize(1600, 900)

        # 读取并解析配置文件
        self.recentOpen = None
        self.initConfig()

        # actions。创建所有action对象，并绑定hanlder
        self.actions = {}
        self.initActions()

        # toolbar
        toolbar = self.initToolbar()
        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

        # menubar
        self.setMenuBar(self.initMenu())

        self.setMouseTracking(True)

        # 初始状态下的widget，点击后打开文件
        self.generateInitWidget()

    def generateInitWidget(self):
        """
        初始界面，仅有”打开文件“和”开始实验“提示
        :return:
        """
        initWidget = QWidget()
        initWidget.setAutoFillBackground(True)
        initLayout = QGridLayout()
        initWidget.setLayout(initLayout)
        # 初始情况下按钮，打开文件和开始实验
        openFileWidget = QPushButton("打开文件(Ctrl+O)", self, objectName="InitButton")
        openFileWidget.clicked.connect(self.onOpenfile)  # button似乎没法绑定action，智能通过connect方式绑定handler
        newLabWidget = QPushButton("开始实验(Ctrl+N)", self, objectName="InitButton")
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
            'action_closefile': ['', '关闭', 'close file', False, self.onCloseFile],
            'action_deletefile': ['', '删除', 'delete file', False, self.onDeleteFile],
            'action_exit': ['', '退出', 'exit', False, self.onExit],
            'action_savefile': ['icons/save.svg', '另存为', 'save', False, self.onSavefile],
            'action_print': ['icons/print.svg', '打印', "print", False, self.onPrint],

            'action_technique': ['icons/technique.svg', '实验技术', "technique", False, self.onTechnique],
            'action_exp_params': ['icons/experparams.svg', "实验参数", 'experimental params', False, self.onExpParams],
            'action_run_exper': ['icons/run.svg', '运行实验', 'run experiment', False, self.onRunExper],
            'action_stop_exper': ['icons/pause.svg', '暂停/继续', 'stop/continue', True, self.onStopExper],
            'action_terminate_exper': ['icons/pause.svg', '终止实验', 'terminate', False, self.onTerminateExper],
            'action_reverse_scan': ['icons/reversescan.svg', '反向扫描', 'reverse scan', False, self.onReverseScan],
            'action_zero_current': ['icons/zerocurrent.svg', 'Zero Current', 'Zero Current', False, self.onZeroCurrent],

            'action_dp_smooth': ['', '数据平滑', 'Smoothing', False, None],  # 平滑
            'action_dp_deriv': ['', '导数', 'Derivatives', False, None],  # 导数
            'action_dp_integrate': ['', '积分', 'Integration', False, None],  # 积分
            'action_dp_semi': ['', '半微分和半积分', 'Semiinteg and Semideriv', False, None],  # 半微分和半积分
            'action_dp_interpolate': ['', '插值', 'Interpolation', False, None],  # 插值
            'action_dp_baseline_fitting': ['', '基线拟合和扣除', 'Baseline Fitting & Subtraction', False, None],
            'action_dp_baseline_correction': ['', '线性基线修正', 'Linear Baseline Correction', False, None],  # 线性基线修正
            'action_dp_fourier_spectrum': ['', '傅里叶频谱', 'Fourier Spectrum', False, None],  # 傅里叶频谱
            'action_dp_fft_filter': ['', '傅里叶滤波', 'FFT Filter', False, None],  # 快速傅里叶变换滤波
            'action_dp_datapoint_remove': ['', '数据点移除', 'Data Point Removing', False, None],  # 数据点移除
            'action_dp_datapoint_modify': ['', '数据点修改', 'Data Point Modifying', False, None],  # 数据点修改
            'action_dp_backgroud_substract': ['', '背景扣除', 'Background Subtraction', False, None],  # 背景扣除
            'action_dp_signal_avg': ['', '信号平均', 'Signal Averaging', False, None],  # 信号平均
            'action_dp_math_ops': ['', '数学运算', 'Mathematical Operation', False, None],  # 数学运算

            'action_show_points': ['', '显示数据点', 'show points', True, self.onShowPoints],
            'action_graphic_option': ['', '图形选项', 'graphic options', False, self.onGraphicOption],
            'action_current_data_graph': ['', '当前数据图', 'current data graph', False, self.onCurrentDataGraph],
            'action_overlay_plotting': ['', '叠加作图', 'overlay plotting', False, self.onOverlayPlotting],
            'action_tiling_plotting': ['', '平铺作图', 'tiling plotting', False, self.onTilingPlotting],
            'action_copy_to_clipboard': ['', '复制到剪切板', 'copy to clipboard', False, self.onCopyToClipboard],
            'action_clear_plot': ['', '清空图像', 'clean plot', False, self.onCleanPlot],
            'action_peak_detect': ['', '峰值检测', 'peak detection', True, self.onPeakDetect],

            'action_data_list': ['', '数据列表', 'data lists', False, self.onDataList],
            'action_data_info': ['', '数据信息', 'data information', False, self.onDataInfo],
            'action_clock': ['', '时钟', 'clock', False, self.onClock],
            'action_new_window': ['', '新窗口', 'new window', False, self.onNewWindow],

            'action_help_topic': ['', '关于主题', 'help topic', False, self.onHelpTopic],
            'action_about': ['', '关于软件', 'about', False, self.onAbout]
        }
        self.actions = {}
        for key in actions_dict:
            value = actions_dict[key]
            action = QAction(QIcon(value[0]), value[1], self)
            action.setStatusTip(value[2])
            action.setCheckable(value[3])
            if value[4] is not None:
                action.triggered.connect(value[4])
            self.actions[key] = action
        # 为打开文件和新建实验设置快捷键
        self.actions['action_openfile'].setShortcut('Ctrl+O')
        self.actions['action_new'].setShortcut('Ctrl+N')

    def initMenu(self):
        menu = self.menuBar()
        menu = QMenuBar(menu)
        # File
        file_menu = menu.addMenu("文件(&F)")

        file_menu.addAction(self.actions['action_new'])
        file_menu.addAction(self.actions['action_openfile'])
        file_menu.addAction(self.actions['action_closefile'])
        file_menu.addAction(self.actions['action_savefile'])
        file_menu.addAction(self.actions['action_deletefile'])
        file_menu.addSeparator()
        for i in range(0, len(self.recentOpen)):
            path = self.recentOpen[i]
            file_menu.addAction('{} {}'.format(i + 1, path))
        file_menu.triggered.connect(self.onOpenRecentFile)
        file_menu.addSeparator()
        file_menu.addAction(self.actions['action_exit'])

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
        graphic_menu.addAction(self.actions['action_current_data_graph'])
        graphic_menu.addAction(self.actions['action_overlay_plotting'])
        graphic_menu.addAction(self.actions['action_tiling_plotting'])
        graphic_menu.addSeparator()
        graphic_menu.addAction(self.actions['action_clear_plot'])
        graphic_menu.addAction(self.actions['action_show_points'])
        graphic_menu.addAction(self.actions['action_peak_detect'])
        graphic_menu.addSeparator()
        graphic_menu.addAction(self.actions['action_graphic_option'])
        graphic_menu.addSeparator()
        graphic_menu.addAction(self.actions['action_copy_to_clipboard'])

        # data process
        data_menu = menu.addMenu("数据处理(&D)")
        data_menu.triggered.connect(self.onDataProcess)
        for action in self.actions:
            if "action_dp" in action:
                data_menu.addAction(self.actions[action])
        self.dpWidgets = self.initDataProcess()  # 数据处理action点击后的弹出窗口

        # analyse
        analyse_menu = menu.addMenu("分析")

        # simulate
        simulate_menu = menu.addMenu("模拟")

        # view
        view_menu = menu.addMenu("视图和窗口(&V)")
        view_menu.addAction(self.actions['action_data_list'])
        view_menu.addAction(self.actions['action_data_info'])
        view_menu.addSeparator()
        view_menu.addAction(self.actions['action_clock'])
        view_menu.addSeparator()
        view_menu.addAction(self.actions['action_new_window'])

        # help
        help_menu = menu.addMenu("帮助(&H)")
        help_menu.addAction(self.actions['action_help_topic'])
        help_menu.addAction(self.actions['action_about'])

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

    def initConfig(self):
        """
        初始化配置文件，配置文件路径由属性configFile决定
        :return:
        """
        self.recentOpen = []
        f = None
        try:
            f = open(self.configFile, 'r', encoding='utf-8')
            data = f.read()
            lines = data.splitlines()
            paths = lines[0].split("=")[1]  # 格式为recent_open:path1,path2,path3
            if len(paths) == 0:
                return
            paths = paths.split(",")
            self.recentOpen = [item for item in paths]
        except:
            return
        finally:
            if f:
                f.close()

    def closeEvent(self, *args, **kwargs):
        """
        窗口关闭时执行的操作。写入配置文件
        :param args:
        :param kwargs:
        :return:
        """
        if len(self.recentOpen) == 0:
            return
        recentSet = list(set(self.recentOpen))[::-1]  # 去重。可能一个文件运行过程中被打开过多次。反转，最近被打开的文件在list最后
        if len(recentSet) > 10:  # 长度太大，则去掉一部分文件
            recentSet = recentSet[:10]
        with open(self.configFile, 'w', encoding='utf-8') as f:
            text = 'recent_open={}'.format(','.join(recentSet))
            f.write(text)

    def onMouseMoved(self, evt):  # event是window的，而不是widget的，似乎没有widget会有event
        vb = self.technique.plotWidget.getPlotItem().vb
        if vb.mapSceneToView(evt):
            point = vb.mapSceneToView(evt)
            x, y = round(point.x(), 4), round(point.y(), 4)
            format1, format2 = "{}={}e{}{}", "{}={}{}"  # E=0.3e-1V, i=0.22A
            curXCarry, curYCarry = self.technique.curXCarry, self.technique.curYCarry
            xKey, xUnit, yKey, yUnit = self.technique.xKey, self.technique.xUnit, self.technique.yKey, self.technique.yUnit
            x = format2.format(xKey, x, xUnit) if curXCarry == 0 else format1.format(xKey, x, curXCarry, xUnit)
            y = format2.format(yKey, y, yUnit) if curYCarry == 0 else format1.format(yKey, y, curYCarry, yUnit)

            self.technique.positionWidget.setText('{}  {}'.format(x, y))

    def onMouseClicked(self, evt: MouseClickEvent):
        if not evt.double():
            return
        vb = self.technique.plotWidget.getPlotItem().vb
        if vb.mapSceneToView(evt.scenePos()):
            point = vb.mapSceneToView(evt.scenePos())
            x, y = round(point.x(), 4), round(point.y(), 4)
            self.dataModifyWindow[(x, y)] = DataModifyWindow(x, y, self)

    def onNew(self):
        # 新建
        self.errInfoWidget.showInfo("can not open com port!")

    def onOpenRecentFile(self, evt):
        # 打开文件方式一，打开最近文件
        # todo file_menu下所有的action都绑定了此handler，只有最近打开文件才会执行
        #  最近打开文件路径的最前边都有一个编号，如"1 C:/acv1.txt"，只有这种格式的才会执行以下解析，否则会return。
        #  也就是说，file_memu下边action除了最近打开文件，都有执行两个handler，目前来看不是一种优雅的实现方式
        if not evt.text()[0].isdigit():
            return
        path = evt.text().split(" ")[1]
        file_type = path.split(".")[-1]
        self.generateMainWidget(path, file_type)

    def onOpenfile(self):
        # 打开文件方式二，访问文件系统并打开文件
        file_path, file_type = QFileDialog.getOpenFileName(self, "选取数据文件", "./", "Files (*.txt *.bin)")
        if file_path is None or len(file_path) == 0:
            warnings.warn('error on open file.')
            return
        self.generateMainWidget(file_path, file_type)

    def parseFile(self, file_path, file_type):
        """

        :param file_path:
        :param file_type:
        :return: 解析出的technique对象；file_data 目前在数据列表上使用，显示文件整体数据
        """
        f, file_data = None, None
        try:
            f = open(file_path, "r")
            file_data = f.read()
        except:
            warnings.warn('文件路径错误：找不到该文件')
            self.errInfoWidget.showInfo("文件路径错误：找不到该文件")
            return
        finally:
            if f:
                f.close()
        if len(file_data) == 0:
            self.errInfoWidget.showInfo('文件无数据')
            return

        lines = file_data.splitlines()

        techniqueName = lines[1]
        # 记录解析时间
        t = time.perf_counter()
        # 找不到任何类型，用抽象类解析
        technique = techniques.interface.AbstractTechnique(self, lines, file_path,
                                                           file_type) if techniqueName not in techniques.implements.techniqueDict else \
        techniques.implements.techniqueDict[techniqueName](self, lines, file_path, file_type)
        print(f'parse({techniqueName}) coast:{time.perf_counter() - t:.8f}s')

        return technique, file_data

    def generateMainWidget(self, file_path, file_type):
        """
        创建主界面，包括图像区域和参数区域，以及坐标区域
        :param file_path:
        :param file_type:
        :return:
        """
        self.technique, self.file_data = self.parseFile(file_path, file_type)  # 解析出的technique对象；目前在数据列表上使用，显示文件整体数据
        self.recentOpen.append(file_path)  # 成功打开后记录

        self.technique.plotWidget.scene().sigMouseMoved.connect(self.onMouseMoved)  # 目前觉得只有window才能够监听鼠标事件
        self.technique.plotWidget.scene().sigMouseClicked.connect(self.onMouseClicked)

        # 主界面初始化
        layout = QGridLayout()

        rightLayout = QVBoxLayout()  # 主界面右侧，展示实验参数
        rightLayout.addWidget(self.technique.parameterWidget)
        layout.addLayout(rightLayout, 0, 1)

        layout.addWidget(self.technique.plotWidget, 0, 0)  # 曲线可视化
        layout.addWidget(self.technique.positionWidget, 1, 0)  # 坐标实时显示

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def onShowPoints(self, state):
        # 显示/隐藏原始数据点
        self.technique.showPoints(state)

    def onGraphicOption(self):
        if self.technique is None or self.centralWidget() is None:
            self.errInfoWidget.showInfo("暂无数据输入!")
            return
        self.popoutRef = GraphicOptionWidget(self, self.technique.basicParams, self.technique.additionalParams,
                                             self.technique.mainPlots)
        self.popoutRef.show()

    def onCurrentDataGraph(self):
        for plot in self.technique.mainPlots:
            self.technique.plotWidget.addItem(plot)  # 这里应该不需要判断item已经存在，因为addItem源码最开始就会帮忙判断，若有则抛出waring并返回，我这里就偷下懒不判断了

    def onPeakDetect(self, state):
        self.technique.peak_detect(state)

    def onOverlayPlotting(self):
        pass

    def onTilingPlotting(self):
        pass

    def onCopyToClipboard(self):
        self.technique.plot_graph()

    def onCleanPlot(self):
        if self.technique.plotWidget is None:
            return
        self.technique.plotWidget.clear()

    def onCloseFile(self):
        widget = self.centralWidget()
        if widget is None:
            return
        widget.close()
        self.generateInitWidget()
        self.technique = None

    def onDeleteFile(self):
        pass

    def onExit(self):
        self.close()

    def onSavefile(self):
        self.popoutRef = PersistCurveWidget(self)
        self.popoutRef.show()

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

    def initDataProcess(self):
        """
        将每一种数据处理绑定一个widget，即每一次点击后的跳出窗口
        :return:
        """
        return {
            '数据平滑': SmoothWidget, '导数': DerivativeWidget, '积分': IntegrateWidget,
            '半积分和半微分': None, '插值': InterpolateWidget, '基线拟合和扣除': BaselineFitWidget,
            '线性基线修正': None, '数据点删除': None, '背景扣除': BackgroundSubtractionWidget,
            '信号平均': SignalAvgWidget, '数学运算': None, '傅里叶频谱': FourierSpectrumWidget,
            '傅里叶滤波': FFTFilterWidget,
        }

    def onDataProcess(self, evt: QAction):
        # 数据处理模块的handler
        print('data process:', evt.text())
        widget = self.centralWidget()
        if widget is None or self.technique is None:
            self.errInfoWidget.showInfo("暂无数据输入!")
            return
        self.popoutRef = self.dpWidgets[evt.text()](self)
        self.popoutRef.show()

    def onDataList(self):
        self.popoutRef = DataListWidget(self)
        self.popoutRef.show()

    def onDataInfo(self):
        self.popoutRef = DataInfoWidget(self)
        self.popoutRef.show()

    def onClock(self):
        self.popoutRef = ClockWidget(self)
        self.popoutRef.show()

    def onNewWindow(self):
        # current_work_dir = os.path.dirname(__file__)
        # path = os.path.join(current_work_dir[:-4], 'main.py')
        # execfile(path)
        self.windowRef = MainWindow()
        self.windowRef.show()

    def onHelpTopic(self):
        pass

    def onAbout(self):
        pass
