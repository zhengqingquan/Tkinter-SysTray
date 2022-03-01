# 读取超时是指客户端等待服务器响应请求的时间。
# 连接超时就是发起请求连接到连接建立之间的最大时长，读取超时就是连接成功开始到服务器返回响应之间等待的最大时长。
# 读取超时是没有默认值的，如果不设置，程序将一直处于等待状态。

import time
import requests
from requests.adapters import HTTPAdapter


def link_timeout_5s():
    url = 'http://www.google.com.hk'

    print(time.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        html = requests.get(url, timeout=5).text  # 设置超时时间为5秒，如果不设置大概21秒超时
        print('success')
    except requests.exceptions.RequestException as e:
        print(e)

    print(time.strftime('%Y-%m-%d %H:%M:%S'))


def link_read_timeout():
    url = 'https://himawari8.nict.go.jp/img/D531106/thumbnail/550/2021/05/18/023000_0_0.png'

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))  # 在http下超时重试3次
    s.mount('https://', HTTPAdapter(max_retries=3))  # 在https下超时重试3次

    print(time.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        r = s.get(url, timeout=5)  # 设置超时时间为5秒，如果不设置大概21秒超时
        print(r.text)
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        return r.text
    except requests.exceptions.RequestException as e:
        print(e)

    print(time.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    link_read_timeout()