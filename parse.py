# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 06.01.2023
#!/usr/bin/ python3

def calculate_odds(odds):
        """Muuttaa moneyline-todennäköisyyden desimaaliksi"""
        if (odds < 0):
            return round((100/-odds),2)
        else: return round(((odds/100)),2)



def both_teams_to_score(x):
    """Luo pelitietueen molemmat joukkueet tekevät maalin -kohteelle"""
    # Haetaan arvot, jos ei löydy asetetaan arvoksi "-"
    try: nimi = x['rows'][0]['name']
    except: nimi = ""
    try: tyyppi = x['rows'][0]['description']
    except: tyyppi = ""
    try: kylla = x['rows'][0]['competitors'][0]['name']
    except: kylla = ""
    try: kylla_odds = calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds'])
    except: kylla_odds = ""
    try: ei = x['rows'][0]['competitors'][1]['name']
    except: ei = ""
    try: ei_odds = calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds'])
    except: ei_odds = ""
    # Rakennetaan tietue
    peli_info = {
                    'nimi': nimi,
                    'tyyppi': tyyppi,
                    'kylla': kylla,
                    'kylla_odds': kylla_odds,
                    'ei': ei,
                    'ei_odds': ei_odds,
                    'msg': ''
                }
    # Viesti tietueelle
    peli_info['msg'] = (
                  str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['kylla']) + " " + str(peli_info['kylla_odds']) + "\n"
                + str(peli_info['ei']) + " " + str(peli_info['ei_odds']) + '\n')
    return peli_info



def one_x_two_builder(x):
    """Luo pelitietueen 1X2, AWAY- ja HOME HANDICAP kohteille"""
    # Haetaan arvot, jos ei löydy asetetaan arvoksi "-"
    try: nimi = x['rows'][0]['name']
    except: nimi = ""
    try: tyyppi = x['rows'][0]['description']
    except: tyyppi = ""
    try: koti = x['rows'][0]['competitors'][0]['name']
    except: koti = ""
    try: koti_odds = calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds'])
    except: koti_odds = ""
    try: vieras = x['rows'][0]['competitors'][1]['name']
    except: vieras = ""
    try: vieras_odds = calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds'])
    except: vieras_odds = ""
    try: tasapeli_odds = calculate_odds(x['rows'][0]['competitors'][2]['odds']['odds'])
    except: tasapeli_odds = ""
    # Rakennetaan tietue
    peli_info = {
                    'nimi': nimi,
                    'tyyppi': tyyppi,
                    'koti': koti,
                    'koti_odds': koti_odds,
                    'vieras': vieras,
                    'vieras_odds': vieras_odds,
                    'tasapeli_odds': tasapeli_odds,
                    'msg': ''
                }
    # Viesti tietueeseen
    peli_info['msg'] = (
                  str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                + "Tasapeli" + " " + str(peli_info['tasapeli_odds']) + '\n'
                + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
    return peli_info



def one_two_builder(x):
    """Luo pelitietueen 12 kohteelle"""
    # Haetaan arvot, jos ei löydy asetetaan arvoksi "-"
    try: nimi = x['rows'][0]['name']
    except: nimi = ""
    try: tyyppi = x['rows'][0]['description']
    except: tyyppi = ""
    try: koti = x['rows'][0]['competitors'][0]['name']
    except: koti = ""
    try: koti_odds = calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds'])
    except:  koti_odds = ""
    try: vieras = x['rows'][0]['competitors'][1]['name']
    except: vieras = ""
    try: vieras_odds = calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds'])
    except: vieras_odds = ""
    # Luodaan tietue
    peli_info = {
                    'nimi': nimi,
                    'tyyppi': tyyppi,
                    'koti': koti,
                    'koti_odds': koti_odds,
                    'vieras': vieras,
                    'vieras_odds': vieras_odds,
                    'msg': ''
                }
    # Viesti tietueelle
    peli_info['msg'] = (
                  str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
    return peli_info



def over_under_builder(x):
    """Luo pelitietueen over/under kohteelle"""
    # Haetaan arvot, jos ei löydy asetetaan arvoksi "-"
    try: nimi = x['rows'][0]['name']
    except: nimi = ""
    try: tyyppi = x['rows'][0]['description']
    except: tyyppi = ""
    try: yli = x['rows'][0]['competitors'][0]['name']
    except: yli = ""
    try: yli_odds = x['rows'][0]['competitors'][0]['odds']['odds']
    except: yli_odds = ""
    try: alle = x['rows'][0]['competitors'][1]['name']
    except: alle = ""
    try: alle_odds = calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds'])
    except: alle_odds = ""
    # Luodaan tietue
    peli_info = {
                    'nimi': nimi,
                    'tyyppi': tyyppi,
                    'yli': yli,
                    'yli_odds': yli_odds,
                    'alle': alle,
                    'alle_odds': alle_odds,
                    'msg': ''
                }
    # Viesti tietueelle
    peli_info['msg'] = (
                  str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                + str(peli_info['yli']) + " " + str(peli_info['yli_odds']) + "\n"
                + str(peli_info['alle']) + " " + str(peli_info['alle_odds']) + '\n')
    return peli_info