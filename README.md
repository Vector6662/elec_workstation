

## python基础

[Python super() 详解 最简单的解释](https://blog.csdn.net/wanzew/article/details/106993425)：mro

## pyqt5

pyqt教程：https://www.pythonguis.com/tutorials/pyqt-layouts/

pyqtgraph使用：https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

中文基本教程：https://maicss.gitbook.io/pyqt-chinese-tutoral/pyqt5/hello_world



The Event Handling Mechanism：https://www.pythonstudio.us/pyqt-programming/the-eventhandling-mechanism.html



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

[closeEvent()重写，添加关闭窗口触发的事件](https://blog.csdn.net/u010139869/article/details/79449315):

🎈widget样式配置：[链接](https://github.com/liweizhong666/PyQt5/blob/master/%E7%BE%8E%E5%8C%96/QPushButton/%E6%8C%89%E9%92%AE%E5%B8%B8%E8%A7%81%E6%A0%B7%E5%BC%8F.py)

## 数据分析

[numpy中的polyfit](https://blog.csdn.net/qq_45804132/article/details/104744632)：polyfit和poly1d

[Numpy.linalg模块的lstsq()进行线性回归拟合(数学建模）](https://blog.csdn.net/weixin_45870904/article/details/111397520)：线性回归，拟合

[python 数据、曲线平滑处理——方法总结(Savitzky-Golay 滤波器、make_interp_spline插值法和convolve滑动平均滤波)](https://blog.csdn.net/weixin_42782150/article/details/107176500)：写了四种平滑的方法

积分、微分：[python 计算离散点的微分和积分(超详细)](https://blog.csdn.net/goodCodeVsBadBs/article/details/108270333)：

### 平滑

https://blog.csdn.net/sinat_39620217/article/details/119645227：里边的描述文字非常好，可以写进论文，比如：

> 使用平滑滤波器对信号滤波时，实际上是拟合了信号中的低频成分，而将高频成分平滑出去了。 如果噪声在高频端，那么滤波的结果就是去除了噪声，反之，若噪声在低频段，那么滤波的结果就是留下了噪声。

最详细：https://blog.csdn.net/weixin_45929124/article/details/123601803



### 微分和积分

复合梯形公式：

https://blog.csdn.net/zhuoqingjoking97298/article/details/107351185，实现的优化，包含推导：https://zhuoqing.blog.csdn.net/article/details/107294049

中心差分（梯度）和向前差分：[Matlab如何求离散点的导数](https://blog.csdn.net/qq_43080446/article/details/108542357)

[纯Python实现：函数求导切线图、求偏导、梯度下降法（4）](https://blog.csdn.net/QLBFA/article/details/107558464)：自行实现求偏导的算法，mark一下， 论文中可以写

龙贝格求积分优化：https://blog.csdn.net/qq_34777600/article/details/79502867

### 贝塞尔曲线

Savitzky-Golay 滤波器：

https://www.cnblogs.com/xiaofengzai/p/15961937.html、https://blog.csdn.net/sinat_21258931/article/details/79298478

b-spline：b样条基函数，用来实现插值。[深入理解贝塞尔曲线](https://juejin.cn/post/6844903666361565191)



### 拟合

最小二乘拟合：

https://www.datarobot.com/blog/ordinary-least-squares-in-python/ 这是api讲解

https://blog.csdn.net/qq_41332314/article/details/127477680 https://blog.csdn.net/m0_38075425/article/details/90738415 推导，两个结合来看

多项式最小二乘拟合：

https://zhuanlan.zhihu.com/p/262254688 包含了实现。

https://geek.digiasset.org/pages/mathbasic/least-squares-polynomial-curve-fitting-python/ 推导比较优秀，比较重要，文中的y_noise其实就是散点y，也就是正式情况下的y，有偏差的y



### 插值

插值：

https://www.aiuai.cn/aifarm1570.html

证明：https://zhuanlan.zhihu.com/p/203408475

https://towardsdatascience.com/b%C3%A9zier-interpolation-8033e9a262c2详细推导，无敌！



### 分数阶微分

半微分和半积分：

分数阶累加的python实现：https://blog.csdn.net/cauchy7203/article/details/107093205/

API：https://github.com/differint/differint/wiki/Main-Functions

### 傅里叶

公式及推导：https://iphysresearch.github.io/blog/post/signal_processing/fft/

傅里叶变换的**频域滤波**：https://blog.csdn.net/sunxmwebstudy/article/details/112762625。比较原理性的，应该对频谱图的平滑、卷积等操作都可以用来滤波。

卷积：https://blog.csdn.net/myangel13141/article/details/115708370，https://blog.csdn.net/whjkm/article/details/81949356



窗函数：[链接](https://blog.hszofficial.site/TutorialForPython/%E7%A7%91%E5%AD%A6%E8%AE%A1%E7%AE%97%E7%AF%87/%E4%BD%BF%E7%94%A8python%E5%81%9A%E8%AE%A1%E7%AE%97/%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E4%BD%BF%E7%94%A8numpy_scipy%E5%A4%84%E7%90%86%E5%A4%8D%E6%9D%82%E7%9A%84%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97%E9%97%AE%E9%A2%98/%E7%AA%97%E5%8F%A3%E5%87%BD%E6%95%B0%E4%B8%8E%E5%8D%B7%E7%A7%AF/%E7%AA%97%E5%8F%A3%E5%87%BD%E6%95%B0%E4%B8%8E%E5%8D%B7%E7%A7%AF.html)。

窗函数理解：https://blog.csdn.net/zhaomengszu/article/details/72627750

窗函数公式：https://blog.csdn.net/qq_44628230/article/details/107003226



傅里叶频谱分析：https://blog.csdn.net/qq_39720178/article/details/124502403

傅里叶变换：

https://blog.csdn.net/sunxmwebstudy/article/details/112762625 实现功能不少



卷积结论证明：[链接](https://aiart.live/courses/%E6%95%B0%E5%AD%97%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86/2022/DIP-2-05%E9%A2%91%E5%9F%9F%E6%BB%A4%E6%B3%A2-1D%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2.pdf)、[如何理解卷积与傅里叶变换的关系？ - 囧程程的回答 - 知乎](https://www.zhihu.com/question/340004682/answer/2004144581) 。



FFT如何做到nlogn的，详细推导：https://blog.csdn.net/qq_43409114/article/details/104870977



### 误差指标

https://cloud.tencent.com/developer/article/2028633

公式参考：https://blog.csdn.net/weixin_39541558/article/details/80705006

### 自动峰检测

https://zhuanlan.zhihu.com/p/549588865



## Aurora安装

Aurora Equation安装教程：https://blog.csdn.net/TycoonL/article/details/115586651

成功，但是莫名其妙：https://www.neusncp.com/user/blog?id=151

伪代码语法：https://zhuanlan.zhihu.com/p/166418214、https://blog.csdn.net/wangh0802/article/details/115608346

aurora原始配置

```
\usepackage{amsmath}
\usepackage{amssymb}
% \usepackage{euler}

\providecommand{\abs}[1]{\left\lvert#1\right\rvert}
\providecommand{\norm}[1]{\left\lVert#1\right\rVert}
```

## MatPlotLib作图参考文档

https://www.runoob.com/matplotlib/matplotlib-line.html

# 论文内容备忘录

------



在论文中需要体现的一些要点：

1. 体现工业软件和工业4.0

2. 基础工业软件国产化







