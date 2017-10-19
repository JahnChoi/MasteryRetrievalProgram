# LoL Champion Mastery Retrieval Program (Riot API)
# 2/15/17

import urllib.request
import urllib.parse
import json
import time


KEY = '*****-********-****-****-****-************'  # Riot API key censored for privacy.
REGION = 'na'
PLATFORM_IDS = {'BR': 'br1', 'EUNE': 'eun1', 'EUW': 'euw1', 'JP': 'jp1',
                'KR': 'kr', 'LAN': 'la1', 'LAS': 'la2', 'NA': 'na1',
                'OCE': 'oc1', 'TR': 'tr1', 'RU': 'ru', 'PBE': 'pbe1'}


# ***************************************
# FORMAT URLS
# ***************************************

def _format_summoner_name(summoner_name: str) -> str:
    '''
    Formats summoner name for URL if summoner name includes a space.
    '''
    if ' ' in summoner_name:
        
        formatted_name = ''
        
        for char in summoner_name:
            
            if char == ' ':
                formatted_name += '%20'
                
            else:
                formatted_name += char
                
    else:
        return summoner_name


def _parse_api_key(url: str) -> str:
    '''
    Returns complete URL to request data.
    '''
    global KEY
    
    return url + urllib.parse.urlencode([('api_key', KEY)])


def _get_champion_list() -> str:
    '''
    Returns URL for champion list.
    '''
    global REGION
    url = 'https://global.api.pvp.net/api/lol/static-data/{}/v1.2/champion?'
    url = url.format(REGION)
    final_url = _parse_api_key(url)

    return final_url


def _get_multiple_summonerID_format_url(summoner_names_list: 'list of summoner names') -> str:
    '''
    Returns URL for retrieving multiple summoner IDs at once.
    '''
    global REGION

    summoners_string = ''
    
    for summoner in summoner_names_list:
        summoner = _format_summoner_name(summoner)
        summoners_string += summoner
        summoners_string += ','

    url = 'https://na.api.pvp.net/api/lol/{}/v1.4/summoner/by-name/{}?'
    url = url.format(REGION, summoners_string)
    final_url = _parse_api_key(url)

    return final_url
    

def _get_summoner_name_format_url(summonerID: str) -> str:
    '''
    Returns URL for summoner name using summoner ID.
    '''
    global REGION

    url = 'https://na.api.pvp.net/api/lol/{}/v1.4/summoner/{}?'
    url = url.format(REGION, summonerID)
    final_url = _parse_api_key(url)

    return final_url


def _get_summonerID_format_url(summoner_name: str) -> str:
    '''
    Returns URL for summoner ID using summoner name.
    '''
    global REGION
    
    url = 'https://na.api.pvp.net/api/lol/{}/v1.4/summoner/by-name/{}?'
    summoner_name = _format_summoner_name(summoner_name)
    url = url.format(REGION, summoner_name)
    final_url = _parse_api_key(url)
    
    return final_url


def _get_currentGame_format_url(region: str, summonerID: str) -> str:
    '''
    Returns URL for current game using region and summoner ID.
    '''
    global PLATFORM_IDS

    url = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{}/{}?'
    url = url.format(PLATFORM_IDS[region.upper()], summonerID)
    final_url = _parse_api_key(url)
    
    return final_url


def _get_champion_mastery_format_url(region: str, summonerID: str, championID: str) -> str:
    '''
    Returns URL for champion mastery using region, summoner ID, and champion ID.
    '''
    global REGION

    url = 'https://na.api.pvp.net/championmastery/location/{}/player/{}/champion/{}?'
    url = url.format(PLATFORM_IDS[region.upper()], summonerID, championID)
    final_url = _parse_api_key(url)

    return final_url


def _get_summoner_rank_format_url(summonerID_list: 'list of summoner IDs') -> str:
    '''
    Returns URL for summoner(s) rank using region summoner ID(s).
    '''
    global REGION

    summonerID_string = ''
    
    for summonerID in summonerID_list:
        summonerID_string += str(summonerID)
        summonerID_string += ','

    summonerID_string = summonerID_string[:-1]

    url = 'https://na.api.pvp.net/api/lol/{}/v2.5/league/by-summoner/{}/entry?'
    url = url.format(REGION, summonerID_string)
    final_url = _parse_api_key(url)

    return final_url


# ***************************************
# REQUESTS
# ***************************************

def _general_request(url: str) -> dict:
    '''
    Returns JSON data from URL.
    '''
    time.sleep(1)
##    print(url)
    http_response = urllib.request.urlopen(url)
    json_string = http_response.read().decode('utf-8')
    json_data = json.loads(json_string)

    return json_data


def request_champion_list() -> dict:
    '''
    Rturns JSON data for all champions.
    '''
    get_url = _get_champion_list()
    json_data = _general_request(get_url)

    return json_data


def request_summoner_name_json(summonerID: str) -> dict:
    '''
    Returns JSON data for summoner name.
    '''
    get_url = _get_summoner_name_format_url(summonerID)
    json_data = _general_request(get_url)

    return json_data


def request_summoner_name_list_json(summoner_names_list: 'list of summoner names') -> dict:
    '''
    Returns JSON data for summoner names list.
    '''
    get_url = _get_multiple_summonerID_format_url(summoner_names_list)
    json_data = _general_request(get_url)

    return json_data
    

def request_summonerID_json(summoner_name: str) -> dict:
    '''
    Returns JSON data for summoner ID.
    '''
    get_url = _get_summonerID_format_url(summoner_name)
    json_data = _general_request(get_url)

    return json_data


def request_currentGame_json(region: str, summonerID: str) -> dict:
    '''
    Returns JSON data for current game.
    '''
    get_url = _get_currentGame_format_url(region, summonerID)
    json_data = _general_request(get_url)

    return json_data


def request_champion_mastery_json(region: str, summonerID: str, championID: str) -> dict:
    '''
    Returns JSON data for summoner's specified champion mastery.
    '''
    get_url = _get_champion_mastery_format_url(region, summonerID, championID)
    json_data = _general_request(get_url)

    return json_data


def request_summoner_ranks_json(summonerID_list: 'list of summoner IDs') -> dict:
    '''
    Returns JSON data for summoner'(s) ranks.
    '''
    try:
        get_url = _get_summoner_rank_format_url(summonerID_list)
        json_data = _general_request(get_url)

    except urllib.error.HTTPError as e:
        
        if e.code == 404:
            return 'All summoners unranked.'
        
        else:
            return 'Status code: {}'.format(e.code)
    
    return json_data
