# coding=utf-8
import requests
from lxml import etree
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

url = "http://account.gyyx.cn/"  # 修改访问服务器主页

user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/76.0.3809.68 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/76.0.3809.12 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/76.0.3809.68 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/75.0.3770.140 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/534.20",
]

headers = {
    "User-Agent": random.choice(user_agent),
    "Referer": url,
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

# 模拟登陆
# @param username 用户名
# @param password 密码
def landing(username, password):
    opt = webdriver.ChromeOptions()
    opt.add_argument('--enable-logging')  # 设置无头 这里加不加这个都行
    # opt.add_argument('--headless')  # 设置无头
    opt.add_argument('--disable-gpu')  # 设置无头
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=opt)
    browser.set_page_load_timeout(4)
    browser.get(url)
    # login_button = browser.find_element_by_xpath('//a[@class="info_mli_a js_alertlogin_a no_lo_a"]').click()
    login_button = browser.find_element_by_xpath('//a[@class="info_mli_a js_alertlogin_a no_lo_a"]')
    login_button.click()
    time.sleep(1)
    account_user = browser.find_element_by_xpath('//input[@class="inps js_Account"]')
    account_user.click()
    account_user.send_keys(username)
    account_password = browser.find_element_by_xpath('//input[@class="inps js_Password"]')
    account_password.click()
    account_password.send_keys(password)
    time.sleep(0.5)
    for i in range(30):
        try:
            click_slice = browser.find_element_by_xpath('//span[@class="nc_iconfont btn_slide"]')
            break
        except:
            time.sleep(0.1)
    actions = ActionChains(browser)
    actions.click_and_hold(click_slice).perform()
    actions.reset_actions()
    actions.move_by_offset(316, 0).perform()
    actions.release()
    login_button = browser.find_element_by_xpath('//input[@class="siginBtn js_passbtn"]')
    login_button.click()
    time.sleep(3)
    print(browser.page_source)
    time.sleep(20)
    browser.quit()
    # req = requests.session()
    # response = req.get(url, headers=headers)
    # html = etree.HTML(response.content.decode())
    # time.sleep(1)


if __name__ == '__main__':
    username = 'aabbcc123a'
    password = 'aabbcc123a'
    landing(username, password)