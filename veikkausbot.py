# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 06.01.2023
#!/usr/bin/ python3
import logging
import requests
import json
import config
import threading
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler
import alerts
import login
import subscription



# Lokit
logging.basicConfig(
    filename='logs.log', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# Vaaditut otsikkotietueet
headers = {
    'Content-type':'application/json',
    'Accept':'application/json',
    'X-ESA-API-Key':'ROBOT'
}



def get_games(session):
    """Funktio hakee pelit Veikkauksen API:sta"""
    global pelit
    try:
        r = session.get('https://www.veikkaus.fi/api/sport-open-games/v1/games/EBET/draws', headers=headers)
    except:
        print('Virhe API yhteydessä')
        return
    # Response objekti dictiin
    response_dict = json.loads(r.text)
    pelit_apu = []
    # Verrataan pelilistaa aiempaan pelilistaan
    for key in response_dict:
        peli_id = key['rows'][0]['eventId']
        pelit_apu.append(peli_id)
    if (set(pelit_apu).difference(set(pelit)) != set()):
        # Spämminesto botin käynnistämisen yhteydessä
        if (len(pelit) == 0):
            pelit=pelit_apu
            return
        # Otetaan mahdollisten uusien pelien id:t talteen 
        else: 
            new_events_ids = set(pelit_apu).difference(set(pelit))
            pelit=pelit_apu
            alerts.AlertClass.alert(new_events_ids, session)
    else: return



def set_interval(func, sec):
    """Funktio asettaa ajastimen pelien hakemiselle"""
    def func_wrapper():
        global s
        set_interval(func, sec)
        get_games(s)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

        


def main() -> None:
    """Main-funktio alustaa botin"""
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", subscription.SubscriptionClass.subscribe))
    dispatcher.add_handler(CommandHandler("stop", subscription.SubscriptionClass.unsubscribe))
    updater.start_polling()
    updater.idle()



# Globals
bot = Bot(config.BOT_TOKEN)
s = login.LoginClass.veikkaus_login(config.VEIKKAUS_USERNAME,config.VEIKKAUS_PASSWORD)
pelit = []
set_interval(get_games, 60)
main()