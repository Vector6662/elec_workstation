最终决定用python完成此任务



[Python super() 详解 最简单的解释](https://blog.csdn.net/wanzew/article/details/106993425)：mro



pyqt教程：https://www.pythonguis.com/tutorials/pyqt-layouts/

pyqtgraph使用：https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

中文基本教程：https://maicss.gitbook.io/pyqt-chinese-tutoral/pyqt5/hello_world



QApplication：每一个app需且仅需一个

event loop：每一个app只有一个

widget：*any* widgets can be windows

In Qt *all* top level widgets are windows -- that is, they don't have a *parent* and are not nested within another widget or layout.

layout：要用一个widget封装一个layout，







event：注意mousemoveevent：

> You'll notice that mouse move events are only registered when you have the button **pressed down**. You can change this by calling `self.setMouseTracking(True)` on the window.

动态折线图：https://www.pythonguis.com/tutorials/plotting-pyqtgraph/#Updating%20the%20plot

一些例子：https://gitee.com/PyQt5/PyQt

[pyqt5窗口内嵌子窗口](https://blog.csdn.net/xinmo_jin/article/details/121928763)

[用pyqt打开和读取文档的方法](https://blog.csdn.net/linZinan_/article/details/115475887)

[10.5 QStackedLayout堆叠布局管理器](https://www.cnblogs.com/yuyingblogs/p/16164631.html)



数据处理：

[numpy中的polyfit](https://blog.csdn.net/qq_45804132/article/details/104744632)：polyfit和poly1d

[Numpy.linalg模块的lstsq()进行线性回归拟合(数学建模）](https://blog.csdn.net/weixin_45870904/article/details/111397520)：线性回归，拟合

[python 数据、曲线平滑处理——方法总结(Savitzky-Golay 滤波器、make_interp_spline插值法和convolve滑动平均滤波)](https://blog.csdn.net/weixin_42782150/article/details/107176500)：写了四种平滑的方法

🎈🎈🎈[python 计算离散点的微分和积分(超详细)](https://blog.csdn.net/goodCodeVsBadBs/article/details/108270333)：





[纯Python实现：函数求导切线图、求偏导、梯度下降法（4）](https://blog.csdn.net/QLBFA/article/details/107558464)：自行实现求偏导的算法，mark一下， 论文中可以写

[Matlab如何求离散点的导数](https://blog.csdn.net/qq_43080446/article/details/108542357)：中心差分（梯度）和向前差分

Savitzky-Golay 滤波器：https://blog.csdn.net/weixin_43821212/article/details/100016021。可以写在论文当中

b-spline：b样条基函数，用来实现插值。[深入理解贝塞尔曲线](https://juejin.cn/post/6844903666361565191)