import tkinter as tk
import pywintypes


class MainWindowCls(tk.Tk):

    def __init__(self):
        super().__init__()  # 继承父类的实例化方法。
        self.update()  # 初始化后刷新窗口数据，否则只有tkinter的初始值。这样会导致找不到顶级窗口句柄。

        # self.hwnd = self.frame()  # 十六进制句柄
        self.hwnd = int(self.frame(), 16)  # 十进制句柄
        # self.hwnd = pywintypes.HANDLE(int(self.frame(), 16))  # class PyHANDLE 句柄
        print(self.hwnd)


if __name__ == '__main__':
    root = MainWindowCls()
    root.mainloop()
