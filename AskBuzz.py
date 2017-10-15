import logging
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, audio, context, session
from utils import buses, dining, tweets, tv, rss, tech_scraper

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def get_alexa_location():
    url = "https://api.amazonalexa.com/v1/devices/{}/settings/address".format(context.System.device.deviceId)
    consent = context.System.user.permissions.consentToken
    header = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(consent)}
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        j = r.json()
        addr = "{l1}, {city}, {state} {postal}".format(l1=j['addressLine1'], city=j['city'], state=j['stateOrRegion'],
                                                       postal=j['postalCode'])
        return addr


def get_login():
    user = session.user['accessToken']
    split = user.split(',')
    username = split[0]
    password = split[1]
    return [username, password]


@ask.intent("GoodWord")
def good_word():
    gw = render_template('GoodWord')
    return statement(gw)


@ask.intent("WhiteGold")
def white_gold():
    wg = render_template('WhiteGold')
    return statement(wg)


@ask.intent("RamblinWreck")
def rambin_wreck():
    rw = render_template('RamblinWreck')
    return statement(rw)


@ask.intent("AlmaMater")
def alma_mater():
    am = render_template('AlmaMater')
    return statement(am)


@ask.intent("GeorgePBurdell")
def george_burdell():
    gp = render_template('GeorgePBurdell')
    return statement(gp)


@ask.intent("MyClasses")
def good_word():
    return statement(tech_scraper.get_str_from_file("Classes"))


@ask.intent("Setup")
def setup():
    myfile = open("data.txt", "w")
    myfile.write("")
    myfile.close()
    user, passw = get_login()
    print("Logging in")
    tech_scraper.login(user, passw)
    print("Setting up Classes")
    tech_scraper.get_classes()
    print("Setting up Meal Swipes")
    tech_scraper.get_meal_swipes()
    print("Setting up Dining Dollars")
    tech_scraper.get_dining_dollars()
    print("Setting up Buzz Funds")
    tech_scraper.get_buzz_funds()
    print("Set up")
    return statement("I'm Ready to make it work!")


@ask.intent("MyMealSwipes")
def good_word():
    return statement(tech_scraper.get_str_from_file("MealSwipes"))


@ask.intent("MyDiningDollars")
def good_word():
    return statement(tech_scraper.get_str_from_file("DiningDollars"))


@ask.intent("MyBuzzFunds")
def good_word():
    return statement(tech_scraper.get_str_from_file("BuzzFunds"))


@ask.intent("AllDiningOpen")
def dining_opens():
    return statement(dining.dining_open())


@ask.intent("GetNews")
def get_news():
    news = rss.get_news(4)
    msg = render_template('News', news=news)
    return statement(msg)


@ask.intent("GetEvents")
def get_events():
    events = rss.get_events(5)
    msg = render_template('Events', events=events)
    return statement(msg)


@ask.intent("DiningHallOpen")
def dining_hall_open(hall=None):
    if hall is None:
        return statement("Please specify a dining hall.")
    if hall.lower() == "north avenue":
        return statement(dining.is_open("north ave")[1])
    if hall.lower() == "britian":
        return statement(dining.is_open("brittain")[1])
    return statement(dining.is_open(hall.lower())[1])


@ask.intent("DiningHallHours")
def dining_hall_hours(hall=None):
    if hall is None:
        return statement("Please specify a dining hall.")
    if hall.lower() == "north avenue":
        return statement(dining.dining_hours("north ave"))
    if hall.lower() == "britian":
        return statement(dining.dining_hours("brittain"))
    return statement(dining.dining_hours(hall.lower()))


@ask.intent("ClassAvg")
def get_class_avg(classname):
    return statement(dining.course_critique(classname))


@ask.intent("NextBus")
def next_bus(col=None):
    if col is None:
        return statement("Please specify a bus route.")
    echo_location = get_alexa_location()
    u = buses.User(echo_location)
    nxt = buses.sort_stops(u.lat, u.lng, col.lower())
    return statement(nxt)


@ask.intent("TwitterUpdates")
def twit():
    twts = tweets.get_tweets('GeorgiaTech', 3)
    msg = render_template('Tweets', tweets=twts)
    return statement(msg)


@ask.intent('WREKRadio')
def wrek_radio():
    speech = "Tuning to Wreck Radio"
    stream_url = "https://gist.githubusercontent.com/Josh-McFarlin/b8811e0e93f5d9e3e37e57a56f86987b/raw/b2b201733b1acbfd65c3005cffd76fa12b4cea1f/WREKRadio.m3u"
    return audio(speech).play(stream_url)


@ask.intent('GTPD')
def gtpd():
    msg = render_template('GTPD')
    return statement(msg)


@ask.intent('TwitterUpdates')
def twit():
    twts = tweets.get_tweets('GeorgiaTech', 3)
    msg = render_template('Tweets', tweets=twts)
    return statement(msg)


@ask.intent('GetChannel')
def channel(chaname):
    tv_channel = tv.find_channel(chaname)
    if tv_channel:
        msg = "{name} is on channel {num}.".format(name=chaname, num=tv_channel)
    else:
        msg = "Sorry, this channel is not available."
    return statement(msg)


@ask.intent('Smoke')
def stop():
    return statement("Baasim Rehan is smoking it up.")


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Pausing WRECK Radio.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming WRECK Radio.').resume()


@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('Stopping WRECK Radio.').clear_queue(stop=True)


if __name__ == '__main__':
    app.run(debug=True)
