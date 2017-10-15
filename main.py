import time
from flask import render_template
from selenium import webdriver
import re

browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")


# browser.implicitly_wait(10)


def login(user, passw):
    browser.get('https://t-square.gatech.edu')
    try:
        url = 'https://login.gatech.edu/cas/login?service=https%3A%2F%2Ft-square.gatech.edu%2Fsakai-login-tool%2Fcontainer'
        browser.get(url)
        username = browser.find_element_by_id("username")
        password = browser.find_element_by_id("password")
        username.send_keys(user)
        password.send_keys(passw)
        browser.find_element_by_name("submit").click()
        time.sleep(5)
        if "portal" not in browser.current_url:
            print("Redirect to Duo")
            doDuo()
    except:
        print("Already logged in.")


def doDuo():
    browser.switch_to_frame("duo_iframe")
    print("Waiting for iFrame load")
    time.sleep(4)
    browser.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div/label/input").click()
    browser.find_element_by_class_name("auth-button").click()
    print("Clicked send Code")
    time.sleep(10)
    print("Hope you clicked it!")


def getClasses():
    classes = []
    for num in range(2, 10):
        try:
            ele = browser.find_element_by_xpath('//*[@id="siteLinkList"]/li[{}]/a'.format(num))
            classes.append(ele.get_attribute("title"))
        except:
            continue
    myfile = open("data.txt", "w")
    myfile.write("Classes:" + render_template('MyClasses', classes=format_classes(classes)))
    myfile.close()


def get_str_from_file(title):
    myfile = open("data.txt", "r")
    lines = myfile.readlines()
    myfile.close()

    for line in lines:
        if title in line:
            return line.split(":")[1]
    return "Couldn't load data; run Setup"


def get_meal_swipes():
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(5)
    left = ""
    try:
        ele = browser.find_element_by_id("blockplanBalance")
        left = ele.text
    except:
        print("frick")

    myfile = open("data.txt", "a")
    myfile.write("\nMealSwipes:" + "You have {} Meal Swipes left".format(left))
    myfile.close()


def get_dining_dollars():
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(10)
    left = ""
    try:
        ele = browser.find_element_by_id("diningpointsBalance")
        left = ele.text
    except:
        print("frick")
    myfile = open("data.txt", "a")
    myfile.write("\nDiningDollars:" + "You have ${} of Dining Dollars left".format(left))
    myfile.close()


def get_buzz_funds():
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(3)
    left = ""
    try:
        ele = browser.find_element_by_id("buzzcardBalance")
        left = ele.text
    except:
        print("frick")

    myfile = open("data.txt", "a")
    myfile.write("\nBuzzFunds:" + "You have {} of Buzzfunds left.".format(left))
    myfile.close()


classChange = {"ENGL": "English", "CHEM": "Chemistry", "MATH": "Math", "PSYCH": "Psychology", "BIO": "Biology",
               "ARCH": "Architecture", "ECE": "Electrical and Computer Engineering", "CS": "Computer Science",
               "HIST": "History",
               "POL": "Politics", "ECON": "Economics", "APPH": "Applied Physiology"}


def format_classes(classes):
    returnclass = []
    for i in range(len(classes)):
        m = re.search('[a-zA-Z]+-\d*', classes[i])
        shortened = m.group(0)
        shortened = shortened.replace('-', ' ')
        classes[i] = shortened
    for thing in classes:
        splitclass = thing.split(" ")
        returnclass.append(classChange[splitclass[0]] + " " + splitclass[1])
    return returnclass
