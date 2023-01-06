# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 05.01.2023
# @Telegram: kwallio
#!/usr/bin/ python3
import logging
import requests
import json
import config
import threading
from telegram import Update, Bot
from telegram.ext import MessageHandler, Updater, CallbackContext, CommandHandler
from datetime import datetime



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



def login (username, password):
    """Sisäänkirjautuminen Veikkauksen tilille palauttaa sessio-objektin"""
    s = requests.Session()
    login_req = {"type":"STANDARD_LOGIN","login":username,"password":password}
    r = s.post("https://www.veikkaus.fi/api/bff/v1/sessions", data=json.dumps(login_req), headers=headers)
    if r.status_code == 200:
        return s
    else:
        raise Exception("Authentication failed", r.status_code)



def alert(uudet_pelit_id, data):
    """Hälytys uudesta pelistä"""
    uudet_pelit_dict = []
    for x in data:
        for y in uudet_pelit_id:
            # Etsitään uusi peli datasta
            if (y == x['id']):
                # Haetaan uuden pelin laji id:n perusteella
                f = open('data/laji.json')
                lajit_data = json.load(f)
                # Jos lajia ei löydy asetetaan arvoksi undefined
                laji = 'undefined'
                for i in lajit_data:
                    if (str(i['id']) == str(x['rows'][0]['sportId'])):
                        laji = i['name']
                # Luodaan peliobjekti uudesta pelistä
                if (x['rows'][0]['type'] == '1X2' or x['rows'][0]['type'] == 'AWAY_HANDICAP' or x['rows'][0]['type'] == 'HOME_HANDICAP'):
                    peli_info = one_x_two_builder(x, laji)
                if (x['rows'][0]['type'] == '12'):
                    peli_info = one_two_builder(x, laji)
                if (x['rows'][0]['type'] == 'BOTH_TEAMS_TO_SCORE'):
                    peli_info = both_teams_to_score(x, laji)
                # Lisätään uusi peli dictiin
                uudet_pelit_dict.append(x)
    # Lähetetään tilaajille viesti uusista peleistä
    with open('data/subscriptions.json', 'r') as subs:
        data = json.load(subs)
        for sub in data:
            for peli in uudet_pelit_dict:
                print(peli)
                bot.send_message(chat_id=int(sub['id']), text=peli_info['msg'])



def both_teams_to_score(x, laji):
    """Luo pelitietueen molemmat joukkueet tekevät maalin -kohteelle"""
    peli_info = {
                    'nimi': x['rows'][0]['name'],
                    'laji': laji,
                    'tyyppi': x['rows'][0]['description'],
                    'kylla': x['rows'][0]['competitors'][0]['name'],
                    'kylla_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                    'ei': x['rows'][0]['competitors'][1]['name'],
                    'ei_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                    'msg': ''
                }
    peli_info['msg'] = ("Uusi peli lisätty:" + "\n"
                + str(peli_info['laji']) + "\n"
                + str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['kylla']) + " " + str(peli_info['kylla_odds']) + "\n"
                + str(peli_info['ei']) + " " + str(peli_info['ei_odds']) + '\n')
    return peli_info



def one_x_two_builder(x, laji):
    """Luo pelitietueen 1X2, AWAY- ja HOME HANDICAP kohteille"""
    peli_info = {
                    'nimi': x['rows'][0]['name'],
                    'laji': laji,
                    'tyyppi': x['rows'][0]['description'],
                    'koti': x['rows'][0]['competitors'][0]['name'],
                    'koti_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                    'vieras': x['rows'][0]['competitors'][1]['name'],
                    'vieras_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                    'tasapeli_odds': calculate_odds(x['rows'][0]['competitors'][2]['odds']['odds']),
                    'msg': ''
                }
    peli_info['msg'] = ("Uusi peli lisätty:" + "\n"
                + str(peli_info['laji']) + "\n"
                + str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                + "Tasapeli" + " " + str(peli_info['tasapeli_odds']) + '\n'
                + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
    return peli_info



def one_two_builder(x, laji):
    """Luo pelitietueen 12 kohteelle"""
    peli_info = {
                    'nimi': x['rows'][0]['name'],
                    'laji': laji,
                    'tyyppi': x['rows'][0]['description'],
                    'koti': x['rows'][0]['competitors'][0]['name'],
                    'koti_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                    'vieras': x['rows'][0]['competitors'][1]['name'],
                    'vieras_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                    'msg': ''
                }
    peli_info['msg'] = ("Uusi peli lisätty:" + "\n" 
                + str(peli_info['laji']) + "\n"
                + str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
    return peli_info



def calculate_odds(odds):
    """Muuttaa moneyline-todennäköisyyden desimaaliksi"""
    if (odds < 0):
        return round((100/-odds),2)
    else: return round(((odds/100)),2)



def get_games(session):
    global pelit
    """Funktio hakee pelit Veikkauksen API:sta"""
    r = session.get('https://www.veikkaus.fi/api/sport-open-games/v1/games/EBET/draws', headers=headers)
    # Response objekti dictiin
    response_dict = json.loads(r.text)
    pelit_apu = []
    # Verrataan pelilistaa aiempaan pelilistaan
    for key in response_dict:
        peli_id = key['id']
        pelit_apu.append(peli_id)
    if (set(pelit_apu).difference(set(pelit)) != set()):
        # Spämminesto botin käynnistämisen yhteydessä
        if (len(pelit) == 0):
            pelit=pelit_apu
            return
        # Otetaan mahdollisten uusien pelien id:t talteen 
        else: 
            new_games_ids = set(pelit_apu).difference(set(pelit))
            pelit=pelit_apu
            alert(new_games_ids, response_dict)
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



def subscribe(update: Update, context: CallbackContext):
    """Lisätään käyttäjä tilaajien listaan"""
    chat_id=update.message.chat_id
    with open('data/subscriptions.json', 'r') as subs:
        data = json.load(subs)
    for sub in data:
        if sub['id'] == chat_id:
            update.message.reply_text('Olet jo tilaaja. Jos haluat poistaa tilauksen, kirjoita /stop.')
            break
    else: 
        with open('data/subscriptions.json', 'r') as subs:
            data = json.load(subs)
            data.append({'id':chat_id})
            with open('data/subscriptions.json', 'w') as subs:
                json.dump(data, subs)
                update.message.reply_text('Tilaus lisätty. Saat jatkossa ilmoituksen ' +
                'uusista pitkävedoista. Jos haluat poistaa tilauksen, kirjoita /stop.')
        


def unsubscribe(update: Update, context: CallbackContext):
    """Poistetaan käyttäjä tilaajien listasta"""
    chat_id=update.message.chat_id
    # Haetaan tilaaja 
    with open('data/subscriptions.json', 'r') as subs:
        data = json.load(subs)
    for sub in range(len(data)):
        if data[sub]['id'] == chat_id:
            del data[sub]
            with open('data/subscriptions.json', 'w') as new_data:
                json.dump(data, new_data)
                update.message.reply_text('Tilaus poistettu. Jos haluat uusia tilauksen ' +
                ', kirjoita /start.')
                break
    else: update.message.reply_text('Et ole vielä tilaaja. Aloittaaksesi tilauksen ' +
                ', kirjoita /start.')
        


def main() -> None:
    """Main-funktio alustaa botin"""
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", subscribe))
    dispatcher.add_handler(CommandHandler("stop", unsubscribe))
    updater.start_polling()
    updater.idle()



# Globals
bot = Bot(config.BOT_TOKEN)
s = login(config.VEIKKAUS_USERNAME,config.VEIKKAUS_PASSWORD)
pelit = []
set_interval(get_games, 30)
main()