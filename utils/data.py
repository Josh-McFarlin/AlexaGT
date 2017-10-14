import time
import datetime
from selenium import webdriver

dining = {
    'north ave': {
        'Monday': '7 AM - 2 AM',
        'Tuesday': '7 AM - 2 AM',
        'Wednesday': '7 AM - 2 AM',
        'Thursday': '7 AM - 2 AM',
        'Friday': '7 AM - 10 PM',
        'Saturday': '10 AM - 10 PM',
        'Sunday': '10 AM - 12 AM'
    },
    'brittain': {
        'Monday': '7 AM - 8 PM',
        'Tuesday': '7 AM - 8 PM',
        'Wednesday': '7 AM - 8 PM',
        'Thursday': '7 AM - 8 PM',
        'Friday': '7 AM - 3 PM',
        'Saturday': 'CLOSED',
        'Sunday': '4 PM - 8 PM'
    },
    'west village': {
        'Monday': '7 AM - 2 AM',
        'Tuesday': '7 AM - 2 AM',
        'Wednesday': '7 AM - 2 AM',
        'Thursday': '7 AM - 2 AM',
        'Friday': '7 AM - 10 PM',
        'Saturday': '8 AM - 10 PM',
        'Sunday': '8 AM - 2 AM'
    }
}


def is_open(dining_hall):
    times = dining[dining_hall][time.strftime("%A")]
    if times == "CLOSED":
        return False, "{} is closed today".format(dining_hall)
    else:
        times = times.split("-")
    for t in range(len(times)):
        times[t] = times[t].strip()
        seperate = times[t].split(" ")
        if t == 0:
            opentime = datetime.datetime.strptime(seperate[0] + ":00", '%H:%M')
            print("Opening: Now = " + str(datetime.datetime.now().time()) + "\nOpening at = " + str(opentime.time()))
            if datetime.datetime.now().time() < opentime.time():
                return False, "{} closed at {} and will not be open until {}".format(dining_hall, times[0].strip(),
                                                                                     times[1].strip())
        elif t == 1:
            close = int(seperate[0])
            if seperate[1] == "PM":
                close += 10
            closetime = datetime.datetime.strptime(str(close) + ":00", '%H:%M')
            print("Closing: Now = " + str(datetime.datetime.now().time()) + "\nClosing at = " + str(closetime.time()))
            if datetime.datetime.now().time() > closetime.time():
                return False, "{} closed at {} and will not be open until {}".format(dining_hall, times[0].strip(),
                                                                                     times[1].strip())
        return True, "{} is open now until {}".format(dining_hall, times[1].strip())


def dining_open():
    openlist = []
    if is_open("north ave")[0]:
        openlist.append("North Ave")
    if is_open("brittain")[0]:
        openlist.append("Brittain")
    if is_open("west village")[0]:
        openlist.append("West Village")
    if len(openlist) == 0:
        return "Nothing is open today"
    elif len(openlist) == 1:
        return "Only {} is open today".format(openlist[0])
    elif len(openlist) == 2:
        return "{} and {} are open today".format(openlist[0], openlist[1])


def dining_hours(hall):
    times = dining[hall][time.strftime("%A")]
    if times == "CLOSED":
        return "{} is closed today".format(hall)
    else:
        times = times.split("-")
    return "{} is open from {} to {}".format(hall, times[0], times[1])


def course_critique(str_class):
    if " " in str_class:
        str_class = str_class.replace(" ", "")
    browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    browser.get("https://critique.gatech.edu/course.php?id={}".format(str_class))
    avg_gpa = browser.find_element_by_xpath("/ html / body / div / div[1] / div / table / tbody / tr / td[2]").text
    browser.quit()
    return "The average grade for {} is {}".format(str_class, avg_gpa)
