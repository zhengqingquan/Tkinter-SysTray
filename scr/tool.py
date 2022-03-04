def byte_conversion(byte):
    """
    输入为一个字节数，返回合适单位的字符串。
    :param byte:
    :return:
    """
    try:
        if byte < 1024:  # 小于1KB以“0000B”的格式返回字符串
            return f'{byte}B'
        elif byte < 1048576:  # 小于1MB，以“0.00KB”的格式返回字符串
            return '{:.2f}KB'.format(byte / 1024)
        elif byte < 1073741824:  # 小于1GB，以“0.00MB”的格式返回字符串
            return '{:.2f}MB'.format(byte / 1024 / 1024)
        else:  # 大于1GB，以“0.00GB”的格式返回字符串
            return '{:.2f}GB'.format(byte / 1024 / 1024 / 1024)
    except TypeError:
        return "未知大小"


def second_conversion(seconds):
    """
    输入一个时间数，单位为秒，返回合适单位的字符串。
    :param seconds:
    :return:
    """
    try:
        if seconds < 10:  # 小于10秒，以“0.00s”的格式返回字符串
            return '{:.2f}s'.format(seconds)
        elif seconds < 60:  # 小于60秒，以“00s”的格式返回字符串
            return f'{int(seconds)}self'
        elif seconds < 3600:  # 小于1小时，以“00m00s“的格式返回字符串
            return f'{int(seconds) // 60}m {int(seconds) % 60}self'
        elif seconds < 216000:  # 小于1天，以"00h00m"的格式返回字符串
            return f'{int(seconds) // 60 // 60}h{int(seconds) // 60 % 60}m'
        else:  # 大于1天，以”00d00h“的格式返回字符串
            return f'{int(seconds) // 60 // 60 // 24}d{int(seconds) // 60 // 60 % 24}h'
    except TypeError:
        return "未知时间"
