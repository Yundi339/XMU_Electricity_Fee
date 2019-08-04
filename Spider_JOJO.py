# -*- coding: utf-8 -*-

import requests
from lxml import etree
from time import time, sleep
from multiprocessing import Process, Queue, Lock
import os, random

save_path = 'img_test/'

home = "https://movie.douban.com"  # 修改访问服务器主页

user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
]

headers = {
    "User-Agent": random.choice(user_agent),
    "Referer": home,
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

def getAll(url_queue, lock):
    while True:
        lock.acquire()
        if not url_queue.empty():
            url, i = url_queue.get()
            lock.release()
            response = requests.get(url, headers=headers)
            html = etree.HTML(response.content)
        else:
            lock.release()
            break
        src_list = html.xpath('//div[@class="cover"]/a/img/@src')
        alt_list = html.xpath('//div[@class="cover"]/a/img/@alt')
        if len(alt_list) == 0:
            alt_list = [str(i) + 'page_'] * len(src_list)
        for src, alt in zip(src_list, alt_list):
            if src[-5] == '.':
                file_name = alt + str(time()) + src[-5:]
            elif src[-4] == '..':
                file_name = alt + str(time()) + src[-4:]
            else:
                file_name = alt + str(time()) + '.jpg'
            img = requests.get(src, headers=headers).content
            print("Downloading: " + file_name + '    ' + src)
            imwrite(save_path + file_name, img)


def imwrite(path, img):
    try:
        with open(path, "wb") as f:
            f.write(img)
            f.close()
        sleep(random.randrange(2, 6))
    except:
        print("==================== SAVE ERROR:%s ====================" % path)


def start(url, pages):
    lock = Lock()
    url_queue = Queue()
    for i in range(0, pages):
        url_queue.put((url + str(i * 30), i))
    r_list = [Process(target=getAll, args=(url_queue, lock)) for i in range(16)]
    [task.start() for task in r_list]
    [task.join() for task in r_list]


if __name__ == '__main__':
    t = time()
    url = 'https://movie.douban.com/subject/11498785/photos?type=S&start='
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    start(url, pages=80)
    print(time() - t)
