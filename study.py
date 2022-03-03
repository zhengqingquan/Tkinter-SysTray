import win32api, win32con, win32gui_struct, win32gui
import tkinter as tk

# https://blog.csdn.net/maqunfi/article/details/82943209
# 参考：https://blog.csdn.net/m0_56708264/article/details/122263286
# win32gui.CreateWindow()

# win32gui.CreatePopupMenu()

# 可能需要两个进程。主进程退出的时候，必须等待子进程全部退出。当前进程和系统托盘的进程应该是同级别的。
class MainUI(object):
    def __init__(self):
        self.root = tk.Tk()  # 创建tk窗口。
        self.root.resizable(True, True)  # 设置窗口x，y方向的可变性。

        self.window_class_name = "SysTrayIconPy"
        self.root.mainloop()  # 开始执行窗口的主循环
        self.create_sys_tray_icon()  # 创建状态栏图标

    # 该方法必须有四个参数
    def notify(self, hwnd, msg, wparam, lparam):
        """鼠标事件"""
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            print("右键弹起")
            # self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            print("左键弹起")
            # self.destroy(exit=0)
        return True

    def create_sys_tray_icon(self):
        icon = 'D:\\1.ico'  # 图标
        hover_text = "SysTrayIcon.py Demo"  # 光标停留显示文字

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh,  # 获得窗口对象的消息
                       win32con.WM_DESTROY: self.destroy,  # 销毁
                       # win32con.WM_COMMAND: self.command,  # 命令，菜单相关
                       win32con.WM_USER + 20: self.notify,  # 通知
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
        win32gui.UpdateWindow(self.hwnd)  # 根据句柄更新窗口

        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        message = win32gui.NIM_ADD  # 增加一个图标到托盘区
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
        win32gui.Shell_NotifyIcon(message, self.notify_id)

        win32gui.PumpMessages()

    def show_window(self):
        self.root.deiconify()  # 显示tk窗口

    def hidden_window(self):
        self.root.withdraw()  # 隐藏tk窗口

        # 刷新系统托盘图标

    def exit(self):
        self.root.destroy()

    def refresh(self):
        pass

    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        print("销毁")
        # nid = (self.hwnd, 0)
        # win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)  # 状态栏删除一个图标
        # win32gui.PostQuitMessage(0)  # 终止应用程序。
        # if exit and self.on_quit:
        #     self.on_quit()  # 需要传递自身过去时用 s.on_quit(s)
        # else:
        #     self.root.deiconify()  # 显示tk窗口


if __name__ == '__main__':
    main = MainUI()

    # main = tk.Tk()
    # main.bind("<Unmap>", lambda event: print('1'))
    # main.mainloop()
