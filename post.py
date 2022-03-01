import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import time
import os


def dl_init():
    """
    Finish
    参考：https://www.cnblogs.com/tianleblog/p/11496177.html
    :return:返回一个连接对象
    """
    requester = requests.Session()  # 打开一个请求会话，为了让request保持连接
    return requester


# 输入为一个字节数，返回合适单位的字符串。
def byte_conversion(byte):
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


# 输入一个时间数，单位为秒，返回合适单位的字符串
def second_conversion(seconds):
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


def download_pic():
    time_start = time.perf_counter()  # 开始时间

    try:
        requester = requests.Session()  # 打开一个请求会话
        requester.mount('http://', HTTPAdapter(max_retries=3))  # 在http下超时重试3次
        requester.mount('https://', HTTPAdapter(max_retries=3))  # 在https下超时重试3次

        url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/shareDirDownload/bDw2maKV'
        proxies = {'http': None, 'https': None}  # 不使用代理
        verify = True  # 开启验证SSL证书
        stream = True  # 不会立马开始下载，默认是False

        responser = requester.get(url=url, proxies=proxies)  # 发送get请求，返回Response对象
        html = etree.HTML(responser.content.decode('utf-8'))  # 使用utf-8编码格式打开HTML文档，并转化成_Element对象
        fixed_token = html.xpath('//*[@id="fixedToken"]/@value')[0]  # 通过xpath获取Token
        print(f'fixedToken为：{fixed_token}')

        time_get_token = time.perf_counter()  # 获取得到Token的时间
        print(f'获取token的时间为：{second_conversion(time_get_token - time_start)}')

        data = {"_method": "POST",
                "data[FileSearch][is_compress]": "false",
                "data[FileSearch][fixedToken]": fixed_token,
                "data[FileSearch][hashUrl]": "bDw2maKV",
                "action": "dir_download_dl",
                "filelist[0]":
                # "/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2021/06-08/02/hima820210608022000fd.png",
                    "/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2022/02-25/08/hima820220225082000fd.png",
                "dl_path":
                # "/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2021/06-08/02/hima820210608022000fd.png"
                    "/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2022/02-25/08/hima820220225082000fd.png"
                }
        url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/fileSearch/download'
        responser = requester.post(url=url, data=data, verify=verify, proxies=proxies,
                                   stream=stream)  # 发送post请求，返回Response对象。

        time_get_download = time.perf_counter()  # 获得得到post响应的时间
        print('下载建立时间为：{:.2f}s'.format(time_get_download - time_get_token))

        print(f'请求状态：{responser.status_code}')
        if responser.status_code == 200:  # 如果请求成功就开始下载
            file_path = os.path.abspath('C:/Users/96400/Desktop/py/hima820210608022000fd2.png')  # 下载时的绝对路径。
            print(f"下载路径为{file_path}")
            chunk_size = 1024  # 每次下载的块大小
            file_size = 0  # 已经写入的文件大小
            pic_size = int(responser.headers['Content-Length'])  # 预下载的文件大小。把字符串类型转为整形，单位：Byte（字节）
            print(f"照片大小为：{byte_conversion(pic_size)}")

            with open(file_path, "wb") as file:  # 文件和文件夹路径必须存在，否则会抛出FileNotFoundError错误。
                print("开始下载")
                for chunk in responser.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    file_size += len(chunk)
                    print(f"\r{byte_conversion(file_size)}/{byte_conversion(pic_size)}", end='')
            if file_size == pic_size:
                print('图片下载完成')

    except requests.exceptions.RequestException as e:
        print(e)  # 输出异常原因。

    time_end = time.perf_counter()  # 结束时间
    print(f'整个下载过程耗时：{second_conversion(time_end - time_start)}')


if __name__ == '__main__':
    pass
    download_pic()
