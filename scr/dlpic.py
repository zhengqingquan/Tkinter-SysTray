import requests
from requests.adapters import HTTPAdapter
import json
import time
from time import strptime
from lxml import etree

from scr.cls import PicCompleteClass
from scr.tool import second_conversion, byte_conversion
from folder import create_folder


# class PicCompleteDlClass(object):
#     def __init__(self, picture):
#         self.picture = picture


def dl_pic_complete():
    # 打开会话
    requester = requests.Session()  # 打开一个请求会话
    requester.mount('http://', HTTPAdapter(max_retries=3))  # 在http下超时重试3次
    requester.mount('https://', HTTPAdapter(max_retries=3))  # 在https下超时重试3次

    # 获取时间
    url = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    responser = requester.get(url)
    latest_time = strptime(json.loads(responser.content.decode("utf-8"))["date"], "%Y-%m-%d %H:%M:%S")

    # 获取token
    url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/shareDirDownload/bDw2maKV'
    responser = requester.get(url=url)  # 发送get请求，返回Response对象
    html = etree.HTML(responser.content.decode('utf-8'))  # 使用utf-8编码格式打开HTML文档，并转化成_Element对象
    fixed_token = html.xpath('//*[@id="fixedToken"]/@value')[0]  # 通过xpath获取Token

    # 实例化类
    pic_complete = PicCompleteClass(time=latest_time, token=fixed_token)

    # 创建文件夹
    create_folder(pic_complete.folder_path)

    # 开始下载
    time_start = time.perf_counter()  # 开始时间
    try:
        proxies = {'http': None, 'https': None}  # 不使用代理
        verify = True  # 开启验证SSL证书
        stream = True  # 不会立马开始下载，默认是False
        responser = requester.post(url=pic_complete.complete_download_url, data=pic_complete.post_data, verify=verify,
                                   proxies=proxies, stream=stream)  # 发送post请求，返回Response对象。

        print(f'请求状态：{responser.status_code}')
        if responser.status_code == 200:  # 如果请求成功就开始下载
            file_path = pic_complete.pic_path  # 下载时的绝对路径。
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

    except requests.exceptions.RequestException as error:
        print(error)  # 输出异常原因。

    time_end = time.perf_counter()  # 结束时间
    print(f'整个下载过程耗时：{second_conversion(time_end - time_start)}')


if __name__ == '__main__':
    dl_pic_complete()
