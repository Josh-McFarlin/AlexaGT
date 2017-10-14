import time
import pickle
from selenium import webdriver
import re
from config import TS_Username, TS_Password


browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")

def login():
    browser.get( 'https://t-square.gatech.edu')
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get( 'https://login.gatech.edu/cas/login?service=https%3A%2F%2Ft-square.gatech.edu%2Fsakai-login-tool%2Fcontainer')
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys(TS_Username)
    password.send_keys(TS_Password)
    browser.find_element_by_name("submit").click()
    time.sleep(5)
    if "portal" not in browser.current_url:
        doDuo()


def doDuo():
    browser.switch_to_frame("duo_iframe")
    time.sleep(4)
    browser.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div/label/input").click()
    browser.find_element_by_class_name("auth-button").click()
    time.sleep(10)
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))




# xPath = '//*[@id="siteLinkList"]/li[6]/a/span/span'
xPath = '//*[@id="siteLinkList"]/li[2]/a/span'
def getClasses():
    login()
    classes = []
   # browser.find_element_by_xpath(xPath).click()
    for num in range(2, 10):
        try:
            ele = browser.find_element_by_xpath('//*[@id="siteLinkList"]/li[{}]/a'.format(num))
            classes.append(ele.get_attribute("title"))
        except:
            continue
    return format_classes(classes)


def format_classes(classes):
    for i in range(len(classes)):
        m = re.search('[a-zA-Z]+-\d*', classes[i])
        shortened = m.group(0)
        shortened = shortened.replace('-', ' ')
        classes[i] = shortened
    return classes


login()