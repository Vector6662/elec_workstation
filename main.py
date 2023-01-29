import sys
from gui.main_window import MainWindow
from PyQt5 import QtWidgets

# 样式，参考：https://github.com/liweizhong666/PyQt5/blob/master/%E7%BE%8E%E5%8C%96/QPushButton/%E6%8C%89%E9%92%AE%E5%B8%B8%E8%A7%81%E6%A0%B7%E5%BC%8F.py
StyleSheet = '''
/*这里是通用设置，所有按钮都有效，不过后面的可以覆盖这个*/

/*
QPushButton#xxx
或者
#xx
都表示通过设置的objectName来指定
*/
QPushButton#InitButton {
    border:none;
    font-size:30px;
    font:bold;
}
QLabel#ErrInfo {
    font-size:25px;
}
QLabel#Title1 {
    font-size:25px;
    font:bold;
}
QLabel#BasicParams {
    font-size:23px;
    color:blue;
}
QLabel#AdditionalParams {
    font-size:23px;
    color:red;
}
QLabel#Position {
    font-size:25px;
    font:bold;
    color:purple;
}
QLabel#Style1 {
    font-size:20px;
    font:bold;
}
'''
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


