import requests
import json
import re


def get_menu(hall):
    url = ""
    if hall == "North Ave":
        url = "https://www.gatechdining.com/smgmenu/json/ga%20tech-north%20ave%20dining%20hall%20-%20other"
    elif hall == "Brittain":
        url = "https://www.gatechdining.com/smgmenu/json/brittain"
    r = requests.get(url)
    text = r.text
    # print(text)
    m = re.search(r'(?<=menuData = .....)(.(?!\]\;))*', text, re.DOTALL)
    print(m.group(0))
    j_str = m.group(0)
    j = json.loads(j_str)
    return j

if __name__ == "__main__":
    m = get_menu("North Ave")
    print(m)
