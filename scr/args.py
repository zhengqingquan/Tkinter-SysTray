import argparse

# 软件名称
PROGRAM_NAME = "himawari8-observer"

# 软件版本
SOFTWARE_VERSION = "1.1.0"

# 日志路径
LOG_PATH = "../scr/log/debug_log.txt"

# 程序的描述
DESCRIPTION = """
            这是参数描述
            """

# 程序参数帮助的结尾。
EPILOG = """
        这是结尾。
        github web: https://github.com/zhengqingquan/himawari8-observer
        """


def arge_init():
    """
    TODO:更多的更完整的命令
    参数解析的初始化
    参考：
        https://blog.csdn.net/MOU_IT/article/details/81782386
        https://www.cnblogs.com/cheyunhua/p/11002421.html
    :return:返回解析器parser
    """
    # 实例化解析器对象
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,  # 程序名
                                     description=DESCRIPTION,  # 参数描述
                                     epilog=EPILOG,  # 结尾描述
                                     usage=argparse.SUPPRESS,  # 关闭用例usage，该值默认为None
                                     add_help=True  # 为解析器默认添加一个-h/--help选项
                                     )
    # 为解析器添加参数
    # 当parse_args()被调用，选项会以"-"前缀识别，剩下的参数则会被假定为位置参数
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=f"%(prog)self {SOFTWARE_VERSION}")

    parser.add_argument("-e",
                        "--equal",
                        type=str,
                        choices=["1d", "4d", "8d", "16d", "20d"],
                        default="4d",
                        const="4d",
                        action="store",
                        dest="equal",
                        nargs="?",
                        help="\"Equal\" represents how many 550-pixel images one side of an image is equal to.")

    parser.add_argument("-o",
                        "--out",
                        default=True,  # 默认为True，表示程序不会自动退出
                        dest="out_state",
                        action="store_false",  # 当输入-o时，变成False，程序将退出
                        help="out program")

    parser.add_argument("-m",
                        "--modify",
                        default=True,
                        action="store_false",  # 默认为False，当输入-e时，变成True
                        help="modify picture, become 12100*12100 pixel")

    parser.add_argument("-dl",
                        "--download",
                        type=str,
                        choices=["complete", "equal"],
                        default="complete",
                        const="complete",
                        dest="dl_way",
                        action="store",
                        nargs="?",
                        help="download way and begin.")
    # parser.error("")  # 用来自定义错误信息。
    return parser


if __name__ == '__main__':
    arge_init()