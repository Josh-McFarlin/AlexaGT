import time
from selenium import webdriver
import re


def login(user, passw):
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
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
            do_duo()
    except:
        print("Already logged in.")


def do_duo():
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    browser.switch_to_frame("duo_iframe")
    print("Waiting for iFrame load")
    time.sleep(4)
    browser.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div/label/input").click()
    browser.find_element_by_class_name("auth-button").click()
    print("Clicked send Code")
    time.sleep(10)
    print("Hope you clicked it!")


def get_classes():
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    classes = []
    for num in range(2, 10):
        try:
            ele = browser.find_element_by_xpath('//*[@id="siteLinkList"]/li[{}]/a'.format(num))
            clas = ele.get_attribute("title")
            if clas != "More Sites":
                classes.append(clas)
        except:
            pass
    classes = format_classes(classes)
    with open("data.txt", "a") as myfile:
        myfile.write("Classes:" + "Your classes are {}.".format(", ".join(classes)))
    browser.close()


def get_str_from_file(title):
    with open("data.txt", "r") as myfile:
        lines = myfile.readlines()

    for line in lines:
        if title in line:
            return line.split(":")[1]
    return "Couldn't load data; run Setup"


def get_meal_swipes():
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(4)
    left = ""
    try:
        ele = browser.find_element_by_id("blockplanBalance")
        left = ele.text
    except:
        print("frick")

    with open("data.txt", "a") as myfile:
        myfile.write("\nMealSwipes:" + "You have {} Meal Swipes left".format(left))
    browser.close()


def get_dining_dollars():
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(4)
    left = ""
    try:
        ele = browser.find_element_by_id("diningpointsBalance")
        left = ele.text
    except:
        print("frick")
    with open("data.txt", "a") as myfile:
        myfile.write("\nDiningDollars:" + "You have ${} of Dining Dollars left".format(left))
    browser.close()


def get_buzz_funds():
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    browser.get("https://mealplan.gatech.edu/dashboard")
    time.sleep(4)
    left = ""
    try:
        ele = browser.find_element_by_id("buzzcardBalance")
        left = ele.text
    except:
        print("frick")

    with open("data.txt", "a") as myfile:
        myfile.write("\nBuzzFunds:" + "You have {} of Buzzfunds left.".format(left))
    browser.close()


classChange = {"ENGL": "English", "CHEM": "Chemistry", "MATH": "Math", "PSYCH": "Psychology", "BIO": "Biology",
               "ARCH": "Architecture", "ECE": "Electrical and Computer Engineering", "CS": "Computer Science",
               "HIST": "History",
               "POL": "Politics", "ECON": "Economics", "APPH": "Applied Physiology", "GT": "GT"}


def format_classes(classes):
    returnclass = []
    for i in range(len(classes)):
        try:
            m = re.search('[a-zA-Z]+[-_]?[\d]{4}(?!\n)', classes[i])
            shortened = m.group(0)
            shortened = shortened.replace('-', ' ')
            shortened = shortened.replace('_', ' ')
            shortened = " ".join(re.split('(\d+)', shortened))
            shortened = shortened.replace("  ", " ")
            classes[i] = shortened
        except:
            pass
    for thing in classes:
        splitclass = thing.split(" ")[:2]
        returnclass.append(classChange[splitclass[0]] + " " + splitclass[1])
    return returnclass
