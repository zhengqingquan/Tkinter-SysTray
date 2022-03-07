import win32con
import win32gui_struct
import win32gui
import win32api

import logging
import threading
from os import path
from time import sleep
from pkg_resources import Requirement
from pkg_resources import resource_filename

from pkg_resources import Requirement
from pkg_resources import resource_filename
from win32api import GetModuleHandle
from win32api import PostQuitMessage
from win32con import CW_USEDEFAULT
from win32con import IDI_APPLICATION
from win32con import IMAGE_ICON
from win32con import LR_DEFAULTSIZE
from win32con import LR_LOADFROMFILE
from win32con import WM_DESTROY
from win32con import WM_USER
from win32con import WS_OVERLAPPED
from win32con import WS_SYSMENU
from win32gui import CreateWindow
from win32gui import DestroyWindow
from win32gui import LoadIcon
from win32gui import LoadImage
from win32gui import NIF_ICON
from win32gui import NIF_INFO
from win32gui import NIF_MESSAGE
from win32gui import NIF_TIP
from win32gui import NIM_ADD
from win32gui import NIM_DELETE
from win32gui import NIM_MODIFY
from win32gui import RegisterClass
from win32gui import UnregisterClass
from win32gui import Shell_NotifyIcon
from win32gui import UpdateWindow
from win32gui import WNDCLASS


class ToastNotifier(object):
    def __init__(self):
        pass

    def show_toast(self):
        # 注册windows窗口
        message_map = {win32con.WM_DESTROY: self.on_destroy, }

        self.wc = win32gui.WNDCLASS()
        self.hInstance = win32api.GetModuleHandle(None)
        self.wc.lpszClassName = str("PythonTaskbar")  # must be a string
        self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
        self.classAtom = win32gui.RegisterClass(self.wc)
        # 参考：https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles
        # 表示这个窗口是个重叠窗口，并且具有菜单。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom, "Taskbar", style,
                                          0, 0, win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, self.hInstance, None)
        win32gui.UpdateWindow(self.hwnd)

        # icon_path = resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
        # hicon = LoadImage(self.hinst, icon_path,
        #                   IMAGE_ICON, 0, 0, icon_flags)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        # 表示拥有图标，拥有消息，拥有提示
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        msg = "Here comes the message"
        title = "Notification"
        nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Tooltip")
        # 添加图标
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

        # 如果触发通知只需要这一步。
        # 修改图标
        # 参考：https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/ns-shellapi-notifyicondataa
        # 修改图标导致触发通知。只要有句柄和设置对应的WM_USER + 20就行。
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                                        WM_USER + 20,
                                                        hicon, "Balloon Tooltip", msg, 200,
                                                        title))
        sleep(10)
        # 这个会触发WM_DESTROY
        DestroyWindow(self.hwnd)
        UnregisterClass(self.wc.lpszClassName, None)
        return None

    def on_destroy(self, hwnd, msg, wparam, lparam):
        print(1)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

        return None


if __name__ == '__main__':
    toast = ToastNotifier()
    toast.show_toast()
