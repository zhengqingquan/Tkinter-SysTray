# import win32api
import win32con
import win32gui_struct
import win32gui


class SysTrayCls(object):
    def __init__(self, root_win):
        self.root_win = root_win  # 传入主窗口
        self.window_class_name = "SysTrayIcon"  # 类名

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh,  # 49361 获得窗口对象的消息
                       win32con.WM_DESTROY: self.destroy,  # 2 销毁
                       win32con.WM_COMMAND: self.command,  # 273 命令
                       win32con.WM_USER + 20: self.notify,  # 1024+20 通知，表示鼠标进入了系统托盘图标的范围。
                       }

        window_class = win32gui.WNDCLASS()  # 实例化窗口类，这个类会被用于注册窗口。
        window_class.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        window_class.lpszClassName = self.window_class_name  # 窗口类的名称
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 1|2 按位或，window_class.style为3。窗口类风格
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        window_class.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷
        window_class.lpfnWndProc = message_map  # 定义窗口处理函数。也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(window_class)  # 根据窗口类注册窗口

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  # 0|524288 指定创建窗口的风格
        handle_instance = win32gui.GetModuleHandle(None)  # 创建窗口，None返回调用进程本身的句柄。
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, handle_instance, None
                                          )
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
        # win32gui.PumpMessages()  # 进入消息循环，处理窗口信息

    def notify(self, hwnd, msg, wparam, lparam):
        """
        该方法必须有四个参数
        :param hwnd:当前接收消息的窗口句柄
        :param msg:被传送过来的消息的ID
        :param wparam:附加在消息上的数据
        :param lparam:附加在消息上的数据
        :return:
        """
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            print("右键弹起")
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            print("左键弹起")

            if self.root_win.state() == "withdrawn":
                self.root_win.state("normal")
                win32gui.SetForegroundWindow(self.root_win.hwnd)  # 将窗口置顶。放到前台。
            elif self.root_win.state() == "iconic":
                self.root_win.state("normal")
                win32gui.SetForegroundWindow(self.root_win.hwnd)  # 将窗口置顶。放到前台。
            elif self.root_win.state() == "normal":
                self.root_win.state("iconic")
            elif self.root_win.state() == "zoomed":
                pass
            else:
                pass

        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()  # 创建弹出菜单。返回值是菜单的句柄。
        option_text = "退出"  # 菜单项的文本
        option_icon = None
        option_id = 5320  # 这是我传入的参数，表示被传入的消息
        item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                        hbmpItem=option_icon,
                                                        wID=option_id)
        win32gui.InsertMenuItem(menu, 0, 1, item)  # 四个参数，菜单项的句柄、位置、位置、指向 MENUITEMINFO 结构的指针，该结构包含有关新菜单项的信息。
        pos = win32gui.GetCursorPos()  # 获取鼠标当前位置的坐标
        win32gui.SetForegroundWindow(self.hwnd)  # 这条语句是必须的。
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def command(self, hwnd, msg, wparam, lparam):
        """
        # 这里估计也是固定四个参数
        :param hwnd:
        :param msg:
        :param wparam:
        :param lparam:
        :return:
        """
        print(msg)
        msg_wdata = win32gui.LOWORD(wparam)
        if msg_wdata == 5320:
            win32gui.DestroyWindow(self.hwnd)  # 这里产生了win32con.WM_DESTROY的消息。
            self.root_win.destroy()

    def destroy(self, hwnd, msg, wparam, lparam):
        """

        :param hwnd:
        :param msg:
        :param wparam:
        :param lparam:
        :return:
        """
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, self.notify_id)

        # 参考：https://blog.csdn.net/qq_38161040/article/details/103099853
        # win32api.PostQuitMessage()

    def destroy2(self):
        """
        正常退出所调用的程序。不应该直接使用destroy
        :return:
        """
        win32gui.DestroyWindow(self.hwnd)

    def refresh(self, hwnd, msg, wparam, lparam):
        """

        :param hwnd:
        :param msg:
        :param wparam:
        :param lparam:
        :return:
        """
        pass

    def __del__(self):
        """

        :return:
        """
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, self.notify_id)


if __name__ == '__main__':
    from MainWindowCls import MainWindowCls

    root = MainWindowCls()
    # systray = SysTrayCls(root)
    root.mainloop()
