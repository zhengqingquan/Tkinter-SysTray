import win32api, win32con, win32gui_struct, win32gui


class SysTrayCls(object):
    def __init__(self, windows):
        self.window_class_name = "SysTrayIconPy"  # 类名
        window_class = win32gui.WNDCLASS()  # 实例化窗口类，这个类会被用于注册窗口。
        window_class.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        window_class.lpszClassName = self.window_class_name  # 窗口类的名称
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 1|2 按位或，window_class.style为3。窗口类风格
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        window_class.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷

        self.classAtom = win32gui.RegisterClass(window_class)  # 根据窗口类注册窗口

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  # 0|524288 指定创建窗口的风格
        handle_instance = win32gui.GetModuleHandle(None)  # 创建窗口，None返回调用进程本身的句柄。
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, handle_instance, None)
        print(self.hwnd)
        # self.hwnd = windows.hwnd
        hover_text = "SysTrayIcon"
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        msg = ""
        time = 500
        title = ""
        self.notify_id = (self.hwnd,  # 接收Windows消息的窗口句柄。
                          0,  # 句柄、托盘图标ID
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                          # 指示结构中的哪些成员包含有效数据
                          # 托盘图标可以使用的功能的标识
                          win32con.WM_USER + 20,  # 回调消息ID， 由用户自定义。与一个自定义的消息处理函数关联。
                          hicon, hover_text,  # 托盘图标句柄、图标字符串
                          msg, time, title,  # 提示内容、以毫秒计的提示显示时间、提示标题
                          win32gui.NIIF_INFO  # 提示用到的图标
                          )
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, self.notify_id)


if __name__ == '__main__':
    from MainWindowCls import MainWindowCls

    root = MainWindowCls()

    systray = SysTrayCls(root)

    root.mainloop()
