import time
from selenium import webdriver
import re
from config import TS_Username, TS_Password

browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")


def login():
    browser.get(
        'https://login.gatech.edu/cas/login?service=https%3A%2F%2Ft-square.gatech.edu%2Fsakai-login-tool%2Fcontainer')

    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")

    username.send_keys(TS_Username)
    password.send_keys(TS_Password)

    browser.find_element_by_name("submit").click()

    time.sleep(5)
    browser.switch_to_frame("duo_iframe")
    browser.find_element_by_class_name("auth-button").click()

    time.sleep(10)


# xPath = '//*[@id="siteLinkList"]/li[6]/a/span/span'
xPath = '//*[@id="siteLinkList"]/li[2]/a/span'
def getClasses():
    """
    login()
    classes = []
   # browser.find_element_by_xpath(xPath).click()
    for num in range(2, 10):
        try:
            ele = browser.find_element_by_xpath('//*[@id="siteLinkList"]/li[{}]/a'.format(num))
            classes.append(ele.get_attribute("title"))
        except:
            continue
    return classes
    """
    return format_classes(['CS-1100-D2', 'CS-1331', 'ENGL-1101-A1,B2,C', 'HIST-2111-A', 'MATH-1552-B1,B2,B3'])


def format_classes(classes):
    for i in range(len(classes)):
        m = re.search('[a-zA-Z]+-\d*', classes[i])
        shortened = m.group(0)
        shortened = shortened.replace('-', ' ')
        classes[i] = shortened
    return classes


if __name__ == "__main__":
    print(getClasses())