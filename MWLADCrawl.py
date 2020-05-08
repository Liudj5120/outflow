'''
毫米波射电天文数据库数据下载程序
环境要求：
1. Chrome Browser (version 81.0.4044.138(official version) (64 bit))
2. Chromedriver.exe(address: http://npm.taobao.org/mirrors/chromedriver/)
'''
import requests
import re
from selenium import webdriver
import time
from pyquery import PyQuery as pq
import os
from retrying import retry
import sys

headers = {'Accept': 'text/html, application/xhtml + xml, application/xml;'
                          'q = 0.9,image/webp, image/apng, */*;q = 0.8, application / signed - exchange; v = b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh; q = 0.9',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) '
                              'AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 75.0.3770.80 Safari / 537.36'
}

# 获取验证码
def getyz(html):
    #获取首页内容
    str1 = str(html)
    #正则表达式的匹配模式
    pattern = 'code/\d+.gif'
    #re.findall查找所有匹配的字符串
    match = re.findall(pattern, str1)
    nums = []
    for e in match:
        temp = re.sub("\D", "", e)
        nums.append(temp)
    yz = "".join(nums)
    #返回验证码
    return yz

# 获取下载链接
def getLinks(url, username, userpwd, driverpath):
    driver = webdriver.Chrome(driverpath)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source

    # 获取验证码
    yz = getyz(html)
    print('验证码：', yz)

    # 自动填充登录信息
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('userpwd').send_keys(userpwd)
    driver.find_element_by_name('yz').send_keys(yz)
    driver.find_element_by_xpath("./*//input[@value='提  交']").click()


    # 自动点击网页弹窗
    alert = driver.switch_to.alert
    at_text = alert.text

    print(at_text)
    alert.accept()

    # 进入下载页面
    driver.get(url + 'downloadclasslist.php')
    down_page = driver.page_source
    down_page1 = pq(down_page)
    hrefs = down_page1('table').find('tbody').find('tr').find('a').items()
    driver.quit()
    return hrefs
    
@retry
# 下载部分
def download(url, hrefs, savepath):
    i = 0
    for href in hrefs:
        down_href = href.attr('href')
        if ('_0508' in down_href) & ('.bur' in down_href):
            if i == 0:
                temp = down_href
            if (i > 0) & (temp == down_href):
                break
            i = i + 1
            down_url = url + down_href
            patern3 = '/'
            filename = re.split(patern3, down_href)
            path = savepath + filename[2]
            
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
                print('\n 已下载：', i, filename[2])
                continue
            else:
                print('\n 正在下载：', i, filename[2])
                chunk_size = 1024
                size = 0
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
    username = '19A004'
    password = '19a004pmo'
    url = 'http://www.radioast.nsdc.cn/'
    savepath = 'D:/mydata/'
    driverpath = 'C:/Program Files (x86)/Google/Chrome/chromedriver_win32/chromedriver.exe'
    hrefs = getLinks(url, username, password, driverpath)
    download(url, hrefs, savepath)

if __name__ == '__main__':
    main()