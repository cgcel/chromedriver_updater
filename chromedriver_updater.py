# -*- coding: utf-8 -*-
# author: elvin


import requests
import subprocess
import re
import zipfile


chrome_location = {
    r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
}

index_url = "http://chromedriver.storage.googleapis.com/?delimiter=/&prefix="
download_url = "http://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip"

mirror_index_url = "http://npm.taobao.org/mirrors/chromedriver/"


class DriverUpdater(object):

    def __init__(self):
        self.get_version()

    def get_version(self):

        for part in chrome_location:

            cmd = r'wmic datafile where name="{}" get Version /value'
            cmd = cmd.format(part)
            output = subprocess.getoutput(cmd)

            if "=" in output:
                self.current_version = output.strip().split("=")[1]
                print("Chrome Location: {}\nChrome Version: {}".format(
                    part, self.current_version))
                break

    def download(self, *path):

        global download_url

        try:
            r = requests.get(index_url, timeout=5)  # 获取版本号列表
            # 根据当前浏览器版本号匹配驱动版本号
            pattern = re.compile(
                r'{}[0-9\.]+'.format(self.current_version.split('.')[0]))
            driver_version = pattern.findall(r.text)[-1]
            print("Driver Version: {}".format(driver_version))

            target_url = download_url.format(driver_version)
            # print(target_url)
            r = requests.get(url=target_url)

            if len(path) == 0:
                file_name = "chromedriver_win32.zip"
                with open(file_name, "wb") as file:
                    print("开始官网下载...", end="")
                    file.write(r.content)
                    print("下载完成")
                    zipfile.ZipFile(file_name).extractall()
                    print("解压完成")

            elif len(path) == 1:
                file_name = path[0] + "\\chromedriver_win32.zip"
                with open(file_name, "wb") as file:
                    print("开始官网下载...", end="")
                    file.write(r.content)
                    print("下载完成")
                    zipfile.ZipFile(file_name).extractall(path[0])
                    print("解压完成")

            else:
                print("只能输入一个路径!")
        except:
            print("官网访问失败, 尝试国内源下载...")
            self.mirror_download(*path)

    def mirror_download(self, *path):
        r = requests.get(mirror_index_url, timeout=5)
        pattern = re.compile(
            r"/mirrors/chromedriver/{}[0-9\.]+".format(self.current_version.split('.')[0]))
        result = pattern.findall(r.text)[-1]
        mirror_download_url = mirror_index_url + \
            '{}/chromedriver_win32.zip'.format(result.split('/')[-1])
        r = requests.get(mirror_download_url)

        if len(path) == 0:
            file_name = "chromedriver_win32.zip"
            with open(file_name, "wb") as file:
                print("开始国内源下载...", end="")
                file.write(r.content)
                print("下载完成")
                zipfile.ZipFile(file_name).extractall()
                print("解压完成")

        elif len(path) == 1:
            file_name = path[0] + "\\chromedriver_win32.zip"
            with open(file_name, "wb") as file:
                print("开始国内源下载...", end="")
                file.write(r.content)
                print("下载完成")
                zipfile.ZipFile(file_name).extractall(path[0])
                print("解压完成")

        else:
            print("只能输入一个路径!")


def main():
    updater = DriverUpdater()
    updater.download()
    # updater.download(".\\drivers")


if __name__ == "__main__":
    main()
