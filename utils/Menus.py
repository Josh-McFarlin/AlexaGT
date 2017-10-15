import requests


def get_menu(hall):
    url = ""
    if hall == "North Ave":
        url = "https://www.gatechdining.com/smgmenu/json/ga%20tech-north%20ave%20dining%20hall%20-%20other"
    elif hall == "Brittain":
        url = "https://www.gatechdining.com/smgmenu/json/brittain"
    r = requests.get(url)
    j = r.json()
    print(j)
    print(j['menuData'])

if __name__ == "__main__":
    m = get_menu("North Ave")
    print(m)
