# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import re  # Python自带的正则表达式模块
import os  # Python自带的模块
import json  # Python自带的模块
import shutil  # Python自带的模块


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。 # 在字符串前面加f表示格式化字符串

    print(r'Hi, {name}\n')  # 在字符串前面加r表示去除转义字符

    response = b'<h1>Hello World!</h1>'  # 在字符串前面加b表示改是bytes类型
    print(response)

    str = u"我是含有中文字符组成的字符串。"  # 在字符串前面加u表示以Unicode格式进行编码

    _VALID_URL = r'''(?x)
                        https?://
                            (?:(?:www|bangumi)\.)?
                            bilibili\.(?:tv|com)/
                            (?:
                                (?:
                                    video/[aA][vV]|
                                    anime/(?P<anime_id>\d+)/play\#
                                )(?P<id_bv>\d+)|
                                video/[bB][vV](?P<id>[^/?#&]+)
                            )
                        '''
    print(_VALID_URL)
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
