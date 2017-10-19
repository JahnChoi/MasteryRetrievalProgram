# LoL Champion Mastery Retrieval Program (User Interface)
# 2/15/17

import riot_api
import outputs
import text_writer
import urllib.error
import json.decoder
import time
import sys

REGION = 'NA'

CHAMPION_JSON_DATA = outputs.ChampionList()


# *****************************
# Trivial Functions
# *****************************

def loading() -> None:
    '''
    Displays loading to make sure program is not frozen.
    '''
    for char in '.....':
        print(char, end='')
        time.sleep(0.5)
        sys.stdout.flush()

    return
    

# *****************************
# User Interface Functions
# *****************************


def enter_summoner_name() -> str:
    '''
    Prompts user to enter summoner name.
    '''
    summoner_name = input('Summoner name: ').lower()
    for char in summoner_name:
        if char in '!@#$%^&*()-<>?;:\'"[]{}+=~`':
            print('Invalid summoner name.')
            print('Please restart.')
    
    return summoner_name


def get_summoner_name(summonerID: str) -> str:
    '''
    Returns summoner name using summoner ID.
    '''
    summoner_name = outputs.SummonerName(summonerID).get_output()

    return summoner_name


def get_summonerID(summoner_name: str) -> str:
    '''
    Returns summoner ID using summoner name.
    '''
    summonerID = outputs.SummonerID(summoner_name).get_output()

    return summonerID


def get_current_game_dict(summoner_name: str) -> dict and list:
    '''
    Returns a dict of summoner IDs (key) and champion IDs (value) and list of summoner names.
    '''
    global REGION
    
    final_dict = dict()

    summonerID = get_summonerID(summoner_name)
    current_game_json = outputs.CurrentGame(REGION, summonerID).get_output()
    summoner_list = current_game_json['participants']
    summoner_names_list = list()
    summoner_ids_list = list()
    
    for summoner in summoner_list:
        final_dict[str(summoner['summonerId'])] = str(summoner['championId'])
        summoner_names_list.append(summoner['summonerName'])
        summoner_ids_list.append(str(summoner['summonerId']))

    return final_dict, summoner_names_list, summoner_ids_list


def get_champion(championID: str) -> str:
    '''
    Returns champion name from champion ID.
    '''
    global CHAMPION_JSON_DATA
    
    champion_name = CHAMPION_JSON_DATA.get_output(championID)

    return champion_name + '\n'


def get_champion_mastery(summonerID: str, championID: str) -> str:
    '''
    Returns champion mastery output.
    '''
    global REGION
    
    champ_mastery = outputs.ChampionMastery(REGION, summonerID, championID).get_output()

    return champ_mastery


def get_summoner_ranks(summonerID_list: 'list of summoner IDs') -> dict:
    '''
    Returns dictionary of summoner
    '''
    summoner_ranks = outputs.SummonerRanks(summonerID_list).get_output()

    return summoner_ranks


def check_for_unranked(summonerID: str, summoner_ranks: dict) -> str:
    '''
    Returns rank of summoner based on summoner name and summoner ranks dictionary.
    '''
    if summonerID in summoner_ranks:
        return 'Rank (SoloQ 5v5): ' + summoner_ranks[summonerID]
        
    else:
        return 'Rank (SoloQ 5v5): (͡°͜ʖ͡°) UNRANKED (͡°͜ʖ͡°)\n'
        

def generate_outputs(print_dict: dict) -> None:
    '''
    Prints a string as a final output.
    '''
    print('**********************************')
    for item in print_dict:
        print()
        print('Summoner: ' + item)
        print(print_dict[item])
        
    return
    

def user_interface() -> None:
    try:
        summoner_name = enter_summoner_name()

        start_time = time.time()    # Starts timer for total execution time
        
        print('Loading', end='')

        summoners_and_champs, summoner_names_list, summoner_ids_list = get_current_game_dict(summoner_name)

        dict_to_print = dict()

        count = 0

        summoner_ranks = get_summoner_ranks(summoner_ids_list)
        
        for summoner in summoners_and_champs:
##            print('Loading ' + summoner, end='')
##            loading()
            print('.', end='')
            sys.stdout.flush()
            dict_to_print[summoner_names_list[count]] = get_champion(summoners_and_champs[summoner]) + \
                                                        check_for_unranked(summoner, summoner_ranks) + \
                                                        get_champion_mastery(summoner, summoners_and_champs[summoner])
            count += 1

        print('\n')
        
        generate_outputs(dict_to_print)
        
    except urllib.error.HTTPError as e:
        print()
        print('**********************************')
        print('Failed to retrieve from Riot API.')
        print('Status code: {}'.format(e.code))
##        if e.code == 404:
##            print(summoner_name + ' is not in a game.')
        print('**********************************')

    except json.decoder.JSONDecodeError:
        print()
        print('**********************************')
        print('Failed to load some JSON data from Riot API.')
        print('Sorry for the inconvenience.')
        print('**********************************')

    try:
        print()
        print('**********************************')
        print('Total execution time:')
        print('--- %s seconds ---' % (time.time() - start_time))
        print('**********************************')
        print()
        print('**********************************')
        print('Champion Mastery Retrieval Program v0.1')
        print('Produced and Created by JahnC')
        print('**********************************')
        print()
        input('Enter to exit program.')
        
    except UnboundLocalError:
        print()
        print('**********************************')
        print('Execution Failure.')
        print('**********************************')
        print()
        print('**********************************')
        print('Champion Mastery Retrieval Program v0.1')
        print('Produced and Created by JahnC')
        print('**********************************')
        print()
        input('Enter to exit program.')

    except NameError:
        print()
        print('**********************************')
        print('Execution Failure.')
        print('**********************************')
        print()
        print('**********************************')
        print('Champion Mastery Retrieval Program v0.1')
        print('Produced and Created by JahnC')
        print('**********************************')
        print()
        input('Enter to exit program.')
    
    return


if __name__ == '__main__':
    user_interface()
