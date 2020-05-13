import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


print("初始化爬蟲引擎 ...")
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
option.add_argument("--headless")

browser = webdriver.Chrome(options=option)

print("載入學在浙大首頁 ...")
browser.get("http://course.zju.edu.cn")

browser.find_element_by_class_name("login-btn").click()
print("跳轉至浙江大學統一認證 ...")

browser.find_element_by_id("username").send_keys("3190106167")
browser.find_element_by_id("password").send_keys("Yuanlin1207!")
browser.find_element_by_id("dl").click()


print("進入 TronClass ...")
browser.find_element_by_class_name("login-btn").click()
time.sleep(3)
browser.find_element_by_link_text('展開更多').click()

print("開始解析待辦事件 ...")
todos = browser.find_elements_by_xpath(
    "//div[@class='todo-list-list']/div")

for t in todos:
    notify(title=t.find_element_by_xpath(
        ".//a/div[@class='todo-title']/div/span[@class='ng-binding']").text,
        subtitle='',
        message=t.find_element_by_xpath(
        ".//a/div[@class='truncate-text']/div/span[contains(text(),'截止日期')]").text)

browser.close()
