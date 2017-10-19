# LoL Champion Mastery Retrieval Program (Outputs)
# 2/15/17

import riot_api

# *****************************
# Functions
# *****************************

def format_summoner_name(summoner_name: str) -> str:
    '''
    Formats summoner names with spaces appropriately when required.
    '''
    formatted_name = ''
    
    for char in summoner_name:
        if char == ' ':
            pass
        else:
            formatted_name += char

    return formatted_name


def check_mastery(mastery_level: int, mastery_points: int) -> str:
    '''
    Returns if you're fucked or not.
    '''
    if mastery_level == 1:
        return 'Easy. Game.'
    elif mastery_level > 1 and mastery_level < 6:
        return 'Getting used to the champion. Shouldn\'t be a problem'
    elif mastery_level == 6:
        return 'Tryharding for mastery level 7. Fuck \'em up.'
    elif mastery_level == 7:
        if mastery_points < 100000:
            return 'Played this champion a shitton. Care.'
        elif mastery_points < 200000:
            return 'Played this champion too much. You\'re probably fucked.'
        elif mastery_points >= 200000:
            return 'Literally it may be better to go fuck yourself than get fucked by this legend.'


# *****************************
# Classes
# *****************************

class ChampionList:
    def __init__(self):
        self._json_data = riot_api.request_champion_list()

    def get_output(self, championID: str) -> str:
        '''
        Returns champion name from champion ID.
        '''
        for champion in self._json_data['data']:
            if self._json_data['data'][champion]['id'] == int(championID):
                return 'Champion: ' + champion


class SummonerName:
    def __init__(self, summonerID: str):
        self._summonerID = summonerID
        self._json_data = riot_api.request_summoner_name_json(summonerID)

    def get_output(self) -> str:
        '''
        Returns summoner name.
        '''
        return self._json_data[self._summonerID]['name']


class SummonerNamesList:
    def __init__(self, summoner_names_list: str):
        self._summoner_names_list = summoner_names_list
        self._json_data = riot_api.request_summoner_name_list_json(summoner_names_list)

    def get_output(self) -> dict:
        '''
        Returns a dict of summoner names (key) and summoner IDs (value) with one request.
        '''
        return_dict = dict()

        for summoner in self._json_data:
            return_dict[self._json_data[summoner]['name']] = str(self._json_data[summoner]['id'])

        return return_dict
        

class SummonerID:
    def __init__(self, summoner_name: str):
        summoner_name = format_summoner_name(summoner_name)
        self._summoner_name = summoner_name.lower()
        self._json_data = riot_api.request_summonerID_json(summoner_name)

    def get_output(self) -> str:
        '''
        Returns integer value of summoner ID.
        '''
        return str(self._json_data[self._summoner_name]['id'])


class CurrentGame:
    def __init__(self, region: str, summonerID: str):
        self._region = region
        self._summonerID = summonerID
        self._json_data = riot_api.request_currentGame_json(region, summonerID)

    def get_output(self) -> str:
        '''
        Returns JSON data of current game.
        '''
        return self._json_data


class ChampionMastery:
    def __init__(self, region: str, summonerID: str, championID: str):
        self._region = region
        self._summonerID = summonerID
        self._championID = championID
        self._json_data = riot_api.request_champion_mastery_json(region, summonerID, championID)

    def get_output(self) -> str:
        '''
        Returns champion mastery level of summoner.
        '''
        champ_level = str(self._json_data['championLevel'])
        total_points = str(self._json_data['championPoints'])
        end_string = check_mastery(int(champ_level), int(total_points))
        final_str = 'Champion Level: ' + champ_level + '\nTotal Mastery: ' + total_points + '\n' + end_string
        
        return final_str


class SummonerRanks:
    def __init__(self, summonerID_list: 'list of summonerIDs'):
        self._summonerID_list = summonerID_list
        self._json_data = riot_api.request_summoner_ranks_json(summonerID_list)

    def get_output(self) -> dict:
        '''
        Returns summoner rank(s).
        Up to 10 summoners at a time.
        '''
        if self._json_data == 'All summoners unranked.':
            return self._json_data
        
        elif type(self._json_data) != dict:
            return self._json_data

        else:
            final_dict = dict()

            for summonerID in self._summonerID_list:
                summonerID = str(summonerID)
                
                if summonerID in self._json_data:
                    summoner_attributes = self._json_data[summonerID][0]['entries'][0]

                    final_dict[summoner_attributes['playerOrTeamId']] = self._json_data[summonerID][0]['tier'] + \
                                                                        ' ' + summoner_attributes['division'] + '\n'

            return final_dict
