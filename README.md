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

积分、微分：[python 计算离散点的微分和积分(超详细)](https://blog.csdn.net/goodCodeVsBadBs/article/details/108270333)：



傅里叶频谱分析：https://blog.csdn.net/qq_39720178/article/details/124502403



复合梯形公式：

https://blog.csdn.net/zhuoqingjoking97298/article/details/107351185，实现的优化，包含推导：https://zhuoqing.blog.csdn.net/article/details/107294049



Savitzky-Golay 滤波器：

https://www.cnblogs.com/xiaofengzai/p/15961937.html、https://blog.csdn.net/sinat_21258931/article/details/79298478

b-spline：b样条基函数，用来实现插值。[深入理解贝塞尔曲线](https://juejin.cn/post/6844903666361565191)

http://t.csdn.cn/ta8su：这个最详细！



中心差分（梯度）和向前差分：[Matlab如何求离散点的导数](https://blog.csdn.net/qq_43080446/article/details/108542357)

[纯Python实现：函数求导切线图、求偏导、梯度下降法（4）](https://blog.csdn.net/QLBFA/article/details/107558464)：自行实现求偏导的算法，mark一下， 论文中可以写



最小二乘拟合：

https://www.datarobot.com/blog/ordinary-least-squares-in-python/ 这是api讲解

https://blog.csdn.net/qq_41332314/article/details/127477680 https://blog.csdn.net/m0_38075425/article/details/90738415 推导，两个结合来看

多项式最小二乘拟合：

https://zhuanlan.zhihu.com/p/262254688 包含了实现。

https://geek.digiasset.org/pages/mathbasic/least-squares-polynomial-curve-fitting-python/ 推导比较优秀，比较重要，文中的y_noise其实就是散点y，也就是正式情况下的y，有偏差的y





插值：

https://www.aiuai.cn/aifarm1570.html

证明：https://zhuanlan.zhihu.com/p/203408475

https://towardsdatascience.com/b%C3%A9zier-interpolation-8033e9a262c2详细推导，无敌！



半微分和半积分：

分数阶累加的python实现：https://blog.csdn.net/cauchy7203/article/details/107093205/



傅里叶变换：

https://blog.csdn.net/sunxmwebstudy/article/details/112762625 实现功能不少







Aurora Equation安装教程：https://blog.csdn.net/TycoonL/article/details/115586651

成功，但是莫名其妙：https://www.neusncp.com/user/blog?id=151

伪代码语法：https://zhuanlan.zhihu.com/p/166418214、https://blog.csdn.net/wangh0802/article/details/115608346



# 论文内容备忘录

------



在论文中需要体现的一些要点：

1. 体现工业软件和工业4.0

2. 基础工业软件国产化