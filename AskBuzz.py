import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, audio, context
from utils import Buses, data
from main import getClasses
import requests

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
    classes = getClasses()
    msg = render_template('MyClasses', classes=classes)
    return statement(msg)


@ask.intent("AllDiningOpen")
def dining_opens():
    return statement(data.diningOpen())


@ask.intent("DiningHallOpen")
def dining_hall_open(hall):
    if hall.lower() == "north avenue":
        return statement(data.isOpen("north ave")[1])
    if hall.lower() == "britian":
        return statement(data.isOpen("brittain")[1])
    return statement(data.isOpen(hall.lower())[1])


@ask.intent("NextBus")
def next_bus(col=None):
    if col is None:
        col = "red"
    echo_location = get_alexa_location()
    u = Buses.User(echo_location)
    nxt = Buses.sort_stops(u.lat, u.lng, col.lower())
    return statement(nxt)


@ask.intent('WREKRadio')
def wrek_radio():
    speech = "Tuning to Wreck Radio"
    stream_url = "https://gist.githubusercontent.com/Josh-McFarlin/b8811e0e93f5d9e3e37e57a56f86987b/raw/b2b201733b1acbfd65c3005cffd76fa12b4cea1f/WREKRadio.m3u"
    return audio(speech).play(stream_url)


@ask.intent('GTPD')
def gtpd():
    msg = render_template('GTPD')
    return statement(msg)


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)


if __name__ == '__main__':
    app.run(debug=True)
