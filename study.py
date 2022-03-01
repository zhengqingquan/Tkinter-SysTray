import win32api, win32con, win32gui_struct, win32gui
import tkinter as tk


# win32gui.CreateWindow()

# win32gui.CreatePopupMenu()

class MainUI(object):
    def __init__(self):
        self.root = tk.Tk()  # 创建tk窗口。
        self.root.resizable(True, True)  # 设置窗口x，y方向的可变性。

        self.window_class_name = "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh,  # 获得窗口对象的消息
                       win32con.WM_DESTROY: self.destroy,  # 销毁
                       # win32con.WM_COMMAND: self.command, # 指令
                       # win32con.WM_USER + 20: self.notify,  # 通知
                       }

        wc = win32gui.WNDCLASS()  # 实例化窗口类，这个类会被用于注册窗口。
        wc.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        wc.lpszClassName = self.window_class_name  # 窗口类的名称
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 窗口类风格
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        wc.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷
        wc.lpfnWndProc = message_map  # 定义窗口处理函数。也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(wc)  # 注册窗口

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  # 指定创建窗口的风格
        handle_instance = win32gui.GetModuleHandle(None)  # 创建窗口，None返回调用进程本身的句柄。
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, handle_instance, None)

        self.root.mainloop()  # 开始执行窗口的主循环

    def show_window(self):
        self.root.deiconify()  # 显示tk窗口

    def hidden_window(self):
        self.root.withdraw()  # 隐藏tk窗口

    def exit(self):
        self.root.destroy()

    def refresh(self):
        pass

    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)  # 状态栏删除一个图标
        win32gui.PostQuitMessage(0)  # 终止应用程序。
        if exit and self.on_quit:
            self.on_quit()  # 需要传递自身过去时用 s.on_quit(s)
        else:
            self.root.deiconify()  # 显示tk窗口


if __name__ == '__main__':
    pass
    main = tk.Tk()
    main.bind("<Unmap>",lambda event:
              print('1')
              )
    main.mainloop()