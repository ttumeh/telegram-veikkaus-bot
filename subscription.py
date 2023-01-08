# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 08.01.2023
#!/usr/bin/ python3
import json
from telegram import Update
from telegram.ext import CallbackContext

class SubscriptionClass:
    def subscribe(update: Update, context: CallbackContext):
        """Lisätään käyttäjä tilaajien listaan"""
        chat_id=update.message.chat_id
        # Tarkistetaan onko käyttäjä jo tilaajana
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