"""
用tkinter创建的窗口默认是不会在系统托盘（状态栏）设置图标的。当我们最小化的时候也只是在任务栏里最小化。也叫做用户提示通知区域
我们需要在系统托盘添加图标，点击图标时显示窗口，最小化的时候关闭窗口。
用户提示通知区域是一个窗口，它有属于自己的句柄。也就是说，当我们点击用户提示区的图标时会传入一个鼠标点击的消息。
系统需要知道你点击了哪个图标，并执行响应的回调函数。这也就是我们点击显示窗口的过程。
而最小化我们可能只需要修改回调函数就行了。
"""
import win32api, win32con, win32gui_struct, win32gui
import os, tkinter as tk


class SysTrayIcon(object):
    """SysTrayIcon类用于显示任务栏图标"""
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 5320

    def __init__(s, icon, hover_text, menu_options, on_quit, tk_window=None, default_menu_index=None,
                 window_class_name=None):
        """
        icon         需要显示的图标文件路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        on_quit      传递退出函数，在执行退出时一并运行
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        default_menu_index 不显示的右键菜单序号
        window_class_name  窗口类名
        """
        s.icon = icon
        s.hover_text = hover_text
        s.on_quit = on_quit  # 把退出的调用传入。
        s.root = tk_window  # 把窗口自身传入。

        menu_options = menu_options + (('退出', None, s.QUIT),)
        s._next_action_id = s.FIRST_ID
        s.menu_actions_by_id = set()  # set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。
        s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        s.menu_actions_by_id = dict(s.menu_actions_by_id)  # dict() 函数用于创建一个字典。
        del s._next_action_id

        s.default_menu_index = (default_menu_index or 0)
        s.window_class_name = window_class_name or "SysTrayIconPy"

        # 参考：https://baike.baidu.com/item/RegisterWindowMessage/877164
        # https://blog.csdn.net/qq_36568418/article/details/80391432
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerwindowmessagea
        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): s.restart,  # 获得窗口对象的消息
                       win32con.WM_DESTROY: s.destroy,  # 退出相关
                       win32con.WM_COMMAND: s.command,  # 菜单相关
                       win32con.WM_USER + 20: s.notify, }  # 这个是由用户定义，用来指定对托盘图标的动作，做出的回调函数
        # 注册窗口类。
        # 参考：https://blog.csdn.net/qq_31243065/article/details/83513795
        # https://docs.microsoft.com/zh-cn/windows/win32/winmsg/window-classes
        # https://docs.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-registerclassa
        # 窗口类是一组属性，系统使用它们作为模板来创建窗口。 每个窗口都是窗口类的成员。
        # wc是WNDCLASS
        wc = win32gui.WNDCLASS()  # 实例化窗口类，这个类会被用于注册窗口。相当于实例化一个结构体，这结构体被用于注册窗口。
        wc.hInstance = win32gui.GetModuleHandle(None)  # 窗口类所在模块的实例句柄
        wc.lpszClassName = s.window_class_name  # 窗口类的名称
        # https://docs.microsoft.com/en-us/windows/win32/winmsg/window-class-styles
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW  # 类风格
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)  # 窗口类的光标
        wc.hbrBackground = win32con.COLOR_WINDOW  # 窗口类的背景画刷
        # 参考：https://docs.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wndproc
        # 参考：https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callwindowproca
        # https://baike.baidu.com/item/lpfnWndProc/8717371
        # 参考：https://blog.csdn.net/m0_56708264/article/details/122263286
        # 这个的意思是，针对不同的消息传递不同的回调函数。
        wc.lpfnWndProc = message_map  # 定义窗口处理函数。也可以指定wndproc.
        s.classAtom = win32gui.RegisterClass(wc)  # 注册窗口

    def activation(s):
        """
        激活任务栏图标，不用每次都重新创建新的托盘图标
        参考：
        https://blog.csdn.net/lizijie7471619/article/details/51058095
        https://baike.baidu.com/item/GetModuleHandle/9598683
        """
        handle_instance = win32gui.GetModuleHandle(None)  # 创建窗口，None返回调用进程本身的句柄。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  # 指定创建窗口的风格
        # 创建窗口，返回句柄
        # 注册窗口后才能创建窗口。
        # 参考：https://www.cnblogs.com/csqtech/p/5573809.html
        # https://www.cnblogs.com/jinxiang1224/p/8468362.html
        s.hwnd = win32gui.CreateWindow(s.classAtom,
                                       s.window_class_name,
                                       style,
                                       0, 0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       0, 0, handle_instance, None)
        win32gui.UpdateWindow(s.hwnd)  # 根据句柄更新某个窗口
        s.notify_id = None
        s.refresh(title='软件已后台！', msg='点击重新打开', time=500)

        # 当窗口创建以后，使用win32gui.PumpMessages()进入无限消息循环，处理窗口消息。
        # 窗口消息首先传递给WndProc，在WndProc中可以定义相应消息的处理过程。
        # 参考：https://blog.csdn.net/MosesAaron/article/details/71407727
        win32gui.PumpMessages()

    def refresh(s, title='', msg='', time=500):
        """
        刷新托盘图标
           title 标题
           msg   内容，为空的话就不显示提示
           time  提示显示时间
        """
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(s.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            # 参考：https://blog.csdn.net/qq_42289041/article/details/90215732
            # 保存图像的对象指针（这里为实例）
            # 资源类型（后）
            # 资源名称
            # 图片拉伸宽度
            # 是否调整 IMAGE 的大小以适应图片
            hicon = win32gui.LoadImage(hinst,
                                       s.icon,
                                       win32con.IMAGE_ICON,
                                       0, 0,
                                       icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        """
            NIM_ADD 增加一个图标到托盘区
            NIM_DELETE 从托盘区删除一个图标
            NIM_MODIFY 修改图标
            NIM_SETFOCUS 将焦点返回托盘区。这个消息通常在托盘区完成了用户界面下的操作后发出。比如一个托盘图标显示一个快捷菜单，然后用户按下ESC键了操作，这是使用NIM_SETFOCUS将焦点继续保留在托盘区。这项仅在系统外壳与常用控制DLL5.0版本以上才可以使用。
            NIM_SETVERSION 指定使用特定版本的系统的外壳与常用控制DLL。缺省值为0，表示使用win95方式。该项仅在系统外壳与常用控制DLL5.0以上版本才能用。
        """
        if s.notify_id:
            message = win32gui.NIM_MODIFY  # 修改图标
        else:
            message = win32gui.NIM_ADD  # 增加一个图标到托盘区
        """
        NIF_ICON：指定hIcon是有效的，（这里设定自定义系统托盘图标必须的）
        NIF_MESSAGE：指定uCallbackMessage是有效的，用于程序接收来自托盘图标的消息，需要自定义一个消息。
        NIF_TIP：指定szTip是有效的，功能是当鼠标移动到图标上时，显示提示信息。
        NIF_INFO：显示气泡通知。
        """
        # 参考：https://blog.csdn.net/say_high/article/details/11092961
        # https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataa
        s.notify_id = (s.hwnd,  # 接收Windows消息的窗口句柄。
                       0,  # 句柄、托盘图标ID
                       win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                       # 指示结构中的哪些成员包含有效数据
                       # 托盘图标可以使用的功能的标识
                       win32con.WM_USER + 20,  # 回调消息ID， 由用户自定义。与一个自定义的消息处理函数关联。
                       hicon, s.hover_text,  # 托盘图标句柄、图标字符串
                       msg, time, title,  # 提示内容、以毫秒计的提示显示时间、提示标题
                       win32gui.NIIF_INFO  # 提示用到的图标
                       )
        # Shell_NotifyIcon是Windows中用来生成系统托盘图标的API函数
        # Shell_NotifyIcon是Windows中用于向任务栏的状态栏发送一个消息。
        # 参考：https://blog.csdn.net/sf9090/article/details/102640368
        # https://baike.baidu.com/item/Shell_NotifyIcon/4842094
        win32gui.Shell_NotifyIcon(message, s.notify_id)

    def show_menu(s):
        """显示右键菜单"""
        # 参考：https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createpopupmenu
        # 如果函数成功，则返回值是新创建的菜单的句柄。
        # 如果函数失败，则返回值为 NULL。
        menu = win32gui.CreatePopupMenu()  # 返回值是创建的弹出菜单的句柄
        s.create_menu(menu, s.menu_options)

        # 参考：https://zhuanlan.zhihu.com/p/264135461
        pos = win32gui.GetCursorPos()  # 获取鼠标当前位置的坐标
        win32gui.SetForegroundWindow(s.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                s.hwnd,
                                None)
        win32gui.PostMessage(s.hwnd, win32con.WM_NULL, 0, 0)

    # 给菜单项添加ID
    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            # 菜单项文本、菜单项图标、菜单项的回调函数。
            option_text, option_icon, option_action = menu_option
            # 如果回调函数是可以调用的，或回调函数在字典中。则添加id和回调函数到字典中。
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result

    def restart(s, hwnd, msg, wparam, lparam):
        s.refresh()

    #
    def destroy(s, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        nid = (s.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 终止应用程序。
        if exit and s.on_quit:
            s.on_quit()  # 需要传递自身过去时用 s.on_quit(s)
        else:
            s.root.deiconify()  # 显示tk窗口

    # 根据通知进行不同的处理。
    def notify(s, hwnd, msg, wparam, lparam):
        """鼠标事件"""
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起，显示菜单
            s.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起，成员方法，销毁自己的状态栏图标
            s.destroy(exit=0)
        return True

    # 创建弹出菜单，参数是弹出菜单的句柄和形式。
    # 参考：https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createpopupmenu
    def create_menu(s, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            print(option_icon)
            print(option_id)
            if option_icon:
                option_icon = s.prep_menu_icon(option_icon)

            if option_id in s.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)  # 插入或追加菜单项
            else: # 这部分应该是子菜单的
                submenu = win32gui.CreatePopupMenu()
                s.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(s, icon):
        # 加载图标。
        # 参考：https://blog.csdn.net/cqyczj/article/details/31846969
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)  # 获取屏幕分辨率
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)  # 获取屏幕分辨率
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        # 参考：https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatibledc
        # https://blog.csdn.net/shellching/article/details/18405185
        # https://blog.csdn.net/schao501917/article/details/52188757
        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    # 参考：https://blog.csdn.net/longwsdy/article/details/111152324
    # 参考：https://blog.csdn.net/seele52/article/details/17542265
    # 参考：https://baike.baidu.com/item/WPARAM/6098975
    # https://www.cnblogs.com/asdyzh/p/9940129.html
    # WPARAM是消息响应机制。
    # WPARAM的高字中（HIWORD(wParam)）是命令的ID号，对菜单来讲就是菜单ID。
    def command(s, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        s.execute_menu_option(id)

    # 右键菜单中的退出。
    def execute_menu_option(s, id):
        menu_action = s.menu_actions_by_id[id]
        if menu_action == s.QUIT:
            win32gui.DestroyWindow(s.hwnd)
        else:
            menu_action(s)


class _Main:  # 调用SysTrayIcon的Demo窗口
    def __init__(s):
        s.SysTrayIcon = None  # 判断是否打开系统托盘图标

    def main(s):
        # tk窗口
        s.root = tk.Tk()  # 创建tk窗口
        # 参考：https://www.cnblogs.com/ylzchs/p/13397914.html
        # https://blog.csdn.net/weixin_42953201/article/details/103063810
        # https://www.cnblogs.com/yang-2018/p/11797151.html
        # Unmap
        # 1. 当组件被取消映射的时候触发该事件
        # 2. 意思是在应用程序中不再显示该组件的时候，例如调用 grid_remove() 方法。
        # 窗口最小化判断，可以说是调用最重要的一步
        # 匿名函数lambda
        # iconic：最小化；normal：正常显示；zoomed：最大化。
        # 参考：https://blog.csdn.net/weixin_39529302/article/details/111736228
        """
        def event():
            s.Hidden_window()
            if s.root.state() == 'iconic':
                
            else
                False
        
        """
        s.root.bind("<Unmap>", lambda event: s.Hidden_window() if s.root.state() == 'iconic' else False)  # 在窗口最小化的时候调用
        # 参考：https://blog.csdn.net/weixin_39967072/article/details/109960087
        s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        # 参考：https://www.jianshu.com/p/451947460531
        s.root.resizable(0, 0)  # 设置窗口x，y方向的可变性。锁定窗口大小不能改变。
        s.root.mainloop()

    def switch_icon(s, _sysTrayIcon, icon='D:\\2.ico'):
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        # 只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon._icon = icon
        _sysTrayIcon.refresh()

        # 气泡提示的例子
        s.show_msg(title='图标更换', msg='图标更换成功！', time=500)

    def show_msg(s, title='标题', msg='内容', time=500):
        s.SysTrayIcon.refresh(title=title, msg=msg, time=time)

    def Hidden_window(s, icon='D:\\1.ico', hover_text="SysTrayIcon.py Demo"):
        """隐藏窗口至托盘区，调用SysTrayIcon的重要函数"""

        # 托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        # 24行有自动添加‘退出’，不需要的可删除
        menu_options = (('一级 菜单', None, s.switch_icon),
                        ('二级 菜单', None, (('更改 图标', None, s.switch_icon),)))

        s.root.withdraw()  # 隐藏tk窗口

        # 在这里实例化SysTrayIcon类
        if not s.SysTrayIcon: s.SysTrayIcon = SysTrayIcon(
            icon,  # 图标
            hover_text,  # 光标停留显示文字
            menu_options,  # 右键菜单
            on_quit=s.exit,  # 退出调用
            tk_window=s.root,  # Tk窗口
        )
        # 激活
        s.SysTrayIcon.activation()

    # tkinter关闭的时候默认会调用destroy()，这里多添加了一个print()函数
    def exit(s, _sysTrayIcon=None):
        s.root.destroy()
        print('exit...')


if __name__ == '__main__':
    Main = _Main()
    Main.main()
