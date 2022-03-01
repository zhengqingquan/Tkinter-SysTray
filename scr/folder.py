"""
folder.py

创建文件夹
"""

import os


def create_folder(folder_path):
    """
    Finish
    判断路径是否存在，若不存在则创建一个。
    :param folder_path:文件夹路径。判断文件夹是否存在，如果不存在则创建一个
    :return:None
    """
    is_exists = os.path.exists(folder_path)  # 用于判断文件夹是否存在（也可以判断某个文件）

    # 用于创建文件夹，若已经存在会抛出FileExistsError
    if not is_exists:
        os.makedirs(folder_path)
    return folder_path


if __name__ == '__main__':
    create_folder("./img/20220301003000/")
