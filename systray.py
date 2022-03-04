import tkinter

import win32api, win32con, win32gui_struct, win32gui


class SysTray(object):
    def __init__(self, class_name=None, icon=None, hover_text=None):
        self._icon = icon or 'D:\\1.ico'  # 图标
        self.hover_text = hover_text or "SysTrayIcon.py Demo"  # 光标停留显示文字
        self.window_class_name = class_name or "SysTrayIconPy"  # 类名

        # notify是获得我们对其的指令，指令执行了销毁。而销毁触发了这里的销毁。
        # 消息会返回五个参数
        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh,  # 49361 获得窗口对象的消息
                       win32con.WM_DESTROY: self.text_arg,  # 2 销毁
                       win32con.WM_COMMAND: self.command,  # 32 命令，菜单相关
                       win32con.WM_USER + 20: self.notify,  # 1024+20 通知
                       }

        wc = win32gui.WNDCLASS()  # 实例化窗口类，这个类会被用于注册窗口。
        wc.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        wc.lpszClassName = self.window_class_name  # 窗口类的名称
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 1|2 按位或，wc.style为3。窗口类风格
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        wc.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷
        wc.lpfnWndProc = message_map  # 定义窗口处理函数。也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(wc)  # 注册窗口

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  # 0|524288 指定创建窗口的风格
        handle_instance = win32gui.GetModuleHandle(None)  # 创建窗口，None返回调用进程本身的句柄。
        print(handle_instance)
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, handle_instance, None)
        print(type(self.hwnd))
        print(self.hwnd)
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
                          hicon, self.hover_text,  # 托盘图标句柄、图标字符串
                          msg, time, title,  # 提示内容、以毫秒计的提示显示时间、提示标题
                          win32gui.NIIF_INFO  # 提示用到的图标
                          )
        win32gui.Shell_NotifyIcon(message, self.notify_id)
        # 参考：https://blog.csdn.net/MosesAaron/article/details/71407727
        # 当窗口创建以后，使用PumpMessages()来让窗口进入消息列表的循环中。否则程序会中止。类似于mainloop()。
        # win32gui.PumpMessages()

    def PumpMessages(self):
        pass

    def text_arg(self, hwnd, msg, wparam, lparam):
        print(hwnd)
        print(msg)
        print(wparam)
        print(lparam)

    # 该方法必须有四个参数
    def notify(self, hwnd, msg, wparam, lparam):
        """鼠标事件"""
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            print("右键弹起")
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            print("左键弹起")
            self.destroy(exit=0)
        return True

    def refresh(self):
        print("refresh")
        pass

    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        nid = (self.hwnd, 0)
        print(self.hwnd)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        # 参考：https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage
        # win32gui.PostQuitMessage(0)  # 终止应用程序。
        print("销毁")
        # nid = (self.hwnd, 0)
        # win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)  # 状态栏删除一个图标
        # win32gui.PostQuitMessage(0)  # 终止应用程序。
        # if exit and self.on_quit:
        #     self.on_quit()  # 需要传递自身过去时用 s.on_quit(s)
        # else:
        #     self.root.deiconify()  # 显示tk窗口

    # 这里估计也是固定四个参数
    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        print(id)
        if id == 5320:
            win32gui.DestroyWindow(self.hwnd)  # 这里产生了win32con.WM_DESTROY的消息。
            print(hwnd)
            print(msg)
            print(wparam)
            print(lparam)
            pass

    def func_pass(self):
        print("pass")
        pass

    def Quit(self):
        pass

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        # menu_options = (('一级 菜单', None, self.func_pass),
        #                 ('二级 菜单', None, (('更改 图标', None, self.func_pass),))) + (('退出', None, 'QUIT'),)
        # s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        # for option_text, option_icon, option_action, option_id in menu_options[::-1]:
        #     if option_icon:
        #         # option_icon = s.prep_menu_icon(option_icon)
        #         pass
        #
        #     # if option_id in s.menu_actions_by_id:
        #     #     item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
        #     #                                                     hbmpItem=option_icon,
        #     #                                                     wID=option_id)
        #     #     win32gui.InsertMenuItem(menu, 0, 1, item)  # 插入或追加菜单项
        #     else:
        #         submenu = win32gui.CreatePopupMenu()
        #         self.show_menu()
        #         item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
        #                                                         hbmpItem=option_icon,
        #                                                         hSubMenu=submenu)
        #         win32gui.InsertMenuItem(menu, 0, 1, item)

        # 包装菜单项信息，包含文本，图标，id。返回值item是结构体 extras是引用。
        option_text = "退出"
        option_icon = None
        option_id = 5320
        item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                        hbmpItem=option_icon,
                                                        wID=option_id)
        win32gui.InsertMenuItem(menu, 0, 1, item)  # 四个参数，菜单项的句柄、位置、位置、指向 MENUITEMINFO 结构的指针，该结构包含有关新菜单项的信息。
        pos = win32gui.GetCursorPos()  # 获取鼠标当前位置的坐标
        win32gui.SetForegroundWindow(self.hwnd) # 将窗口置顶。放到前台。
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    # 析构函数
    # 在跳出作用域的时候会执行一次
    def __del__(self):
        # win32gui.PostQuitMessage(0)  # 终止应用程序。
        print("析构函数")


if __name__ == '__main__':
    sys_tray = SysTray()
    root = tkinter.Tk()
    root.mainloop()
    win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, sys_tray.notify_id)
    del sys_tray
    # RefreshTrayIcon()
    # sys_tray.PumpMessages()

    # import win32con, win32gui
    # import pywintypes
    # import tkinter

    # hwnd = win32gui.FindWindow(None, u"窗口名称")
    # root = tkinter.Tk()
    # root.update()
    # print(root.winfo_toplevel())
    # hwnd = pywintypes.HANDLE(int(root.frame(), 16))
    # print(win32gui.GetWindowText(hwnd))
    # print(win32gui.GetClassName(hwnd))
    # print(root.frame())
    # print(hwnd)
    # root.mainloop()

    # root = tkinter.Tk()
    # root.update()  # 必须更新
    #
    # tk_top = win32gui.FindWindow("TkTopLevel", root.title())
    # print(tk_top)
    # root.mainloop()
