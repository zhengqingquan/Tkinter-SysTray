import tkinter as tk
from SysTrayCls import SysTrayCls


# import pywintypes


class MainWindowCls(tk.Tk):

    def __init__(self):
        super().__init__()  # 继承父类的实例化方法。
        # self.protocol('WM_DELETE_WINDOW', self.exit_window)  # 点击Tk窗口关闭时直接调用自身的exit_window()方法，不使用默认关闭。
        self.update()  # 初始化后刷新窗口数据，否则只有tkinter的初始值。这样会导致找不到顶级窗口句柄。

        # self.hwnd = self.frame()  # 十六进制句柄
        self.hwnd = int(self.frame(), 16)  # 十进制句柄
        # self.hwnd = pywintypes.HANDLE(int(self.frame(), 16))  # class PyHANDLE 句柄

        # 创建系统托盘图标
        self.systray = SysTrayCls(self)

    def exit_window(self):
        """

        :return:
        """
        self.withdraw()  # 隐藏tk窗口


if __name__ == '__main__':
    root = MainWindowCls()
    root.mainloop()