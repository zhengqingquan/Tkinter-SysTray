import tkinter as tk
import os
import win32api, win32con, win32gui_struct, win32gui

# 参考：https://pypi.org/project/pywin32/

"""
    可能的鼠标事件：
    WM_MOUSEMOVE      #光标经过图标
    WM_LBUTTONDOWN    #左键按下
    WM_LBUTTONUP      #左键弹起
    WM_LBUTTONDBLCLK  #双击左键
    WM_RBUTTONDOWN    #右键按下
    WM_RBUTTONUP      #右键弹起
    WM_RBUTTONDBLCLK  #双击右键
    WM_MBUTTONDOWN    #滚轮按下
    WM_MBUTTONUP      #滚轮弹起
    WM_MBUTTONDBLCLK  #双击滚轮
"""

class SysTray(object):
    def __init__(self,tray_icon,hover_text,menu_options):
        # 注册窗口类
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        wc.lpszClassName = self.window_class_name  # 窗口类的名称
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 类风格
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        wc.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷
        wc.lpfnWndProc = message_map  # 也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(wc)

class MainUI(object):
    def __init__(self):
        self.root = tk.Tk()  # 创建tk窗口。
        self.root.resizable(True, True)  # 设置窗口x，y方向的可变性。
        self.root.mainloop()  # 开始执行窗口的主循环

    def show_window(self):
        self.root.deiconify()  # 显示tk窗口

    def hidden_window(self):
        self.root.withdraw()  # 隐藏tk窗口

    def exit(self):
        self.root.destroy()

if __name__ == '__main__':
    # main_ui = MainUI()
    # main_ui.show_window()



