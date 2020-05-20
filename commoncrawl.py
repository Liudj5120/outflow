'''
普通数据下载程序
支持断点续传，显示进度条
'''
import requests
import re
from selenium import webdriver
import time
from pyquery import PyQuery as pq
import os
from retrying import retry
import sys
@retry
def download(url, savepath, savename):
    down_url = url
    filename = savename
    path = savepath + filename
    try:
        response = requests.get(down_url, stream=True, verify=False, timeout = 5)
    except requests.exceptions.RequestException as e:
        print(e)    
    total_size = int(response.headers['Content-Length'])
    if os.path.exists(path):
        temp_size = os.path.getsize(path)  
    else:
        temp_size = 0   
    if temp_size == total_size:
        print('\n 下载完成', filename)
    else:
        headers = {'Range': 'bytes=%d-' % temp_size}
        print('\n 正在下载：', filename)
        chunk_size = 1024
        size = temp_size
        response = requests.get(url, stream=True, verify=False, headers=headers)

        with open(path, 'wb') as file:
            for data in response.iter_content(chunk_size = chunk_size):
                file.write(data)
                file.flush()
                size = len(data) + size
                # 进度条
                length = 40
                done = int(length * size / total_size)
                sys.stdout.write("\r[%s%s] [%.2f%%] [%.2f]MB" % ('█' * done, '  ' * (length - done), 100 * size / total_size, round(size / chunk_size / 1024, 2)))

def main():
    link1 = 'https://irsa.ipac.caltech.edu/applications/wise/servlet/Download?file=%24%7Bcache-dir%7D%2FAF-irsasearchops.ipac-ibedatawiseallwisep3am_cdd0808470847p318_ac510847p318_ac51-w1-int-3--1025969470.fits&return=WISE-Multi-Color-Blue.fits&log=true&'
    link2 = 'https://irsa.ipac.caltech.edu/applications/wise/servlet/Download?file=%24%7Bcache-dir%7D%2FAF-irsasearchops.ipac-ibedatawiseallwisep3am_cdd0808470847p318_ac510847p318_ac51-w2-int-3--1025969470.fits&return=WISE-Multi-Color-Green.fits&log=true&'
    link3 = 'https://irsa.ipac.caltech.edu/applications/wise/servlet/Download?file=%24%7Bcache-dir%7D%2FAF-irsasearchops.ipac-ibedatawiseallwisep3am_cdd0808470847p318_ac510847p318_ac51-w3-int-3--1025969470.fits&return=WISE-Multi-Color-Red.fits&log=true&'
    savepath = 'D:/'
    savename = 'green'
    download(link2, savepath, savename)

if __name__ == '__main__':
    main()