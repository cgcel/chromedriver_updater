# -*- coding: utf-8 -*-
# author: elvin


import requests
import subprocess
import re
import zipfile
import os


chrome_location = {
    r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
}

index_url = "http://chromedriver.storage.googleapis.com/?delimiter=/&prefix="

download_url = "http://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip"


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

    def download_driver(self, *location):

        global download_url

        r = requests.get(index_url)  # 获取版本号列表
        # 根据当前浏览器版本号匹配驱动版本号
        pattern = re.compile(
            r'{}[0-9\.]+'.format(self.current_version.split('.')[0]))
        driver_version = pattern.findall(r.text)[-1]
        print("Driver Version: {}".format(driver_version))

        target_url = download_url.format(driver_version)
        # print(target_url)
        r = requests.get(url=target_url)

        if len(location) == 0:
            file_name = "chromedriver_win32.zip"
            with open(file_name, "wb") as file:
                print("开始下载...", end="")
                file.write(r.content)
                print("下载完成")
                zipfile.ZipFile(file_name).extractall()
                print("解压完成")

        elif len(location) == 1:
            file_name = location[0] + "chromedriver_win32.zip"
            with open(file_name, "wb") as file:
                print("开始下载...", end="")
                file.write(r.content)
                print("下载完成")
                zipfile.ZipFile(file_name).extractall()
                print("解压完成")
            
        else:
            print("只能输入一个路径!")


def main():
    updater = DriverUpdater()
    updater.download_driver()
    # updater.download_driver("..\\test\\")

    subprocess.Popen("pause", shell=True)


if __name__ == "__main__":
    main()
