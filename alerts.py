# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 08.01.2023
#!/usr/bin/ python3
import time
import json
import parse




def alert(uudet_pelit_id, session, bot, headers):
    """Hälytys uudesta pelistä"""
    for event_id in uudet_pelit_id:
        kohteet = []
        print(event_id)
        try:
            r = session.get(f'https://www.veikkaus.fi/api/sport-open-games/v1/games/ebet/draws/by-event/{event_id}', headers=headers)
        except:
            print('Virhe API-yhteydessä')
            return
        response_dict = json.loads(r.text)
        # Haetaan API-vastausta parin minuutin ajan lisäkohteiden toivossa
        # (purkkakorjaus Veikkauksen API:n sync-ongelmalle)
        # TODO: Queue + thread?
        timeout = time.time() + 180
        while True:
            if (time.time() > timeout):
                break
            time.sleep(5)
            #print('Odotetaan...')
            try:
                r = session.get(f'https://www.veikkaus.fi/api/sport-open-games/v1/games/ebet/draws/by-event/{event_id}', headers=headers)
            except:
                print('Virhe API-yhteydessä')
            response_dict_new = json.loads(r.text)
            if (len(response_dict) < len(response_dict_new)):
                #print('Lisää kohteita löytyi')
                response_dict = response_dict_new
                continue
            else: continue
        for kohde in response_dict:
            # Luo tietue 12-kohteelle
            if (kohde['rows'][0]['type'] == '12'):
                peli_info = parse.one_two_builder(kohde)
                kohteet.append(peli_info)
            # Luo tietue HANDICAP ja 1X2 kohteille
            if (kohde['rows'][0]['type'] == '1X2' or kohde['rows'][0]['type'] == 'AWAY_HANDICAP' 
                or kohde['rows'][0]['type'] == 'HOME_HANDICAP'):
                peli_info = parse.one_x_two_builder(kohde)
                kohteet.append(peli_info)
            # Luo tietue yli/alle kohteille
            if (kohde['rows'][0]['type'] == 'OVER_UNDER'):
                peli_info = parse.both_teams_to_score(kohde)
                kohteet.append(peli_info)
            # Luo tietue "Molemmat tekevät maalin kohteille"
            if (kohde['rows'][0]['type'] == 'BOTH_TEAMS_TO_SCORE'):
                peli_info = parse.over_under_builder(kohde)
                kohteet.append(peli_info)
        if (len(kohteet) > 0):
            # Lähetetään viesti tilaajille
            with open('data/subscriptions.json', 'r') as subs:
                data = json.load(subs)
                msg = '\n'.join([str(elem['msg']) for elem in kohteet])
                for sub in data:
                    bot.send_message(chat_id=int(sub['id']), text="Uusi kohde lisätty \n\n" + msg)
        else:
            with open('data/subscriptions.json', 'r') as subs:
                data = json.load(subs)
                for sub in data:
                    bot.send_message(chat_id=int(sub['id']), text="Tunnistamaton kohde lisätty: \n\n" + event_id)