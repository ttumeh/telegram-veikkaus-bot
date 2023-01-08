# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 06.01.2023
#!/usr/bin/ python3

def calculate_odds(odds):
        """Muuttaa moneyline-todennäköisyyden desimaaliksi"""
        if (odds < 0):
            return round((100/-odds),2)
        else: return round(((odds/100)),2)


class ParserClass:
    def both_teams_to_score(x):
        """Luo pelitietueen molemmat joukkueet tekevät maalin -kohteelle"""
        peli_info = {
                        'nimi': x['rows'][0]['name'],
                        'tyyppi': x['rows'][0]['description'],
                        'kylla': x['rows'][0]['competitors'][0]['name'],
                        'kylla_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                        'ei': x['rows'][0]['competitors'][1]['name'],
                        'ei_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                        'msg': ''
                    }
        peli_info['msg'] = (
                      str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                    + str(peli_info['kylla']) + " " + str(peli_info['kylla_odds']) + "\n"
                    + str(peli_info['ei']) + " " + str(peli_info['ei_odds']) + '\n')
        return peli_info



    def one_x_two_builder(x):
        """Luo pelitietueen 1X2, AWAY- ja HOME HANDICAP kohteille"""
        peli_info = {
                        'nimi': x['rows'][0]['name'],
                        'tyyppi': x['rows'][0]['description'],
                        'koti': x['rows'][0]['competitors'][0]['name'],
                        'koti_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                        'vieras': x['rows'][0]['competitors'][1]['name'],
                        'vieras_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                        'tasapeli_odds': calculate_odds(x['rows'][0]['competitors'][2]['odds']['odds']),
                        'msg': ''
                    }
        peli_info['msg'] = (
                      str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                    + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                    + "Tasapeli" + " " + str(peli_info['tasapeli_odds']) + '\n'
                    + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
        return peli_info



    def one_two_builder(x):
        """Luo pelitietueen 12 kohteelle"""
        peli_info = {
                        'nimi': x['rows'][0]['name'],
                        'tyyppi': x['rows'][0]['description'],
                        'koti': x['rows'][0]['competitors'][0]['name'],
                        'koti_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                        'vieras': x['rows'][0]['competitors'][1]['name'],
                        'vieras_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                        'msg': ''
                    }
        peli_info['msg'] = (
                      str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                    + str(peli_info['koti']) + " " + str(peli_info['koti_odds']) + "\n"
                    + str(peli_info['vieras']) + " " + str(peli_info['vieras_odds']) + '\n')
        return peli_info



    def over_under_builder(x):
        """Luo pelitietueen over/under kohteelle"""
        peli_info = {
                        'nimi': x['rows'][0]['name'],
                        'tyyppi': x['rows'][0]['description'],
                        'yli': x['rows'][0]['competitors'][0]['name'],
                        'yli_odds': calculate_odds(x['rows'][0]['competitors'][0]['odds']['odds']),
                        'alle': x['rows'][0]['competitors'][1]['name'],
                        'alle_odds': calculate_odds(x['rows'][0]['competitors'][1]['odds']['odds']),
                        'msg': ''
                    }
        peli_info['msg'] = (
                      str(peli_info['nimi'] + " " + str(peli_info['tyyppi']) + "\n")
                    + str(peli_info['yli']) + " " + str(peli_info['yli_odds']) + "\n"
                    + str(peli_info['alle']) + " " + str(peli_info['alle_odds']) + '\n')
        return peli_info