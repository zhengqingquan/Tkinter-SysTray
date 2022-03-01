"""
图片分为两种下载方式，拼图方式和完整方式。
拼图方式（puzzle way）：图片在下载过程中会被分为多份，分别下载，最后再合成为一张完整的图片。
完整方式（complete way）：图片在下载过程中就是一张完整的图片。
"""
from time import strftime


class PicPuzzle(object):
    """
    拼图方式（puzzle way）：图片在下载过程中会被分为多份，分别下载，最后再合成为一张完整的图片。
    """
    puzzle_download_url = 'https://himawari8.nict.go.jp/img/D531106'  # 碎片下载方式使用的url，不应该被修改

    def __init__(self, time, equal):
        """
        根据传入的时间和图片碎片数量来构造图片实例。
        :param time:照片的时间。
        :param equal:str类型，从程序参数传入。意为被等分为多少块，例如：20d
        """
        arr_equal = {"1d": 1, "4d": 4, "8d": 8, "16d": 16, "20d": 20}
        self.str_equal = equal  # 被等分为多少块，str类型，例如：20d
        self.int_equal = arr_equal.get(self.str_equal)  # 照片被等分为多少块，int类型，例如：20


class PicCompleteClass(object):
    """
    完整方式（complete way）：图片在下载过程中就是一张完整的图片。
    """
    token_get_url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/shareDirDownload/bDw2maKV'  # 获取Token时使用的url
    complete_download_url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/fileSearch/download'  # 完整下载方式使用的url
    post_data = {}  # 使用post下载时候的data数据。
    suffix = "png"  # 图片类型后缀
    pic_size = 0  # 图片大小
    dl_finish = False  # 图片下载完成标志位

    def __init__(self, time, token=""):
        """
        根据传入的时间和图片碎片数量来构造图片实例。
        :param time:照片的时间。
        :param token:下载时使用的令牌
        """

        self.year = strftime("%Y", time)  # 年
        self.month = strftime("%m", time)  # 月
        self.day = strftime("%d", time)  # 日
        self.hour = strftime("%H", time)  # 时
        self.minute = strftime("%M", time)  # 分
        self.seconds = strftime("%S", time)  # 秒

        self.post_token = token  # Token

        # 存储图片时顶级路径的文件夹名称，例如：img
        # 用于下载时保存的文件夹名称，可以修改。
        self.folder_top = "img"

        # 存储图片时根目录路径的文件夹名称，例如：20210515052000
        # 用于下载时保存的文件夹名称，可以修改。
        self.folder_root = f"{self.year}{self.month}{self.day}{self.hour}{self.minute}{self.seconds}"

        # 存储图片时文件夹的相对路径，例如.img/20210515052000
        # 用于下载前创建文件夹，不建议直接修改。
        self.folder_path = f"./{self.folder_top}/{self.folder_root}"

        # 完整下载方式下，最终的图片名，例如：hima820210608022000fd.png
        # 用于下载时保存的图片名称，可以修改。
        self.pic_name = f"hima8" \
                        f"{self.year}{self.month}{self.day}{self.hour}{self.minute}{self.seconds}fd.{self.suffix}"

        # 完整下载方式下，图片保存的相对路径，例如：..img/20210515052000/hima820210608022000fd.png
        # 用于下载时保存的图片相对路径，不建议直接修改。
        self.pic_path = f"{self.folder_path}/{self.pic_name}"

        # 构建post
        self.build_mapping()

    def build_mapping(self):
        # 完整下载方式下，用于构建post请求中的图片名称，例如：hima820210608022000fd.png
        # 用于下载时使用的图片名称，不应该修改。
        pic_name = f"hima8" \
                   f"{self.year}{self.month}{self.day}{self.hour}{self.minute}{self.seconds}fd.{self.suffix}"

        self.post_data = {"_method": "POST",
                          "data[FileSearch][is_compress]": "false",
                          "data[FileSearch][fixedToken]": f"{self.post_token}",
                          "data[FileSearch][hashUrl]": "bDw2maKV",
                          "action": "dir_download_dl",
                          "filelist[0]":
                              f"/osn-disk/webuser/wsdb/share_directory/bDw2maKV/{self.suffix}/Pifd/"
                              f"{self.year}/{self.month}-{self.day}/{self.hour}/{pic_name}",
                          "dl_path":
                              f"/osn-disk/webuser/wsdb/share_directory/bDw2maKV/{self.suffix}/Pifd/"
                              f"{self.year}/{self.month}-{self.day}/{self.hour}/{pic_name}"
                          }

    def print_self(self):
        print(f"{self.pic_path}")
        for key in self.post_data.keys():
            print(f"{key}:{self.post_data[key]}")


if __name__ == '__main__':
    import requests
    import json
    from time import strptime

    url = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    responser = requests.get(url)
    latest_time = strptime(json.loads(responser.content.decode("utf-8"))["date"], "%Y-%m-%d %H:%M:%S")
    pic_complete = PicCompleteClass(latest_time)
    pic_complete.print_self()
