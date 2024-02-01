import requests
from datetime import datetime, timezone, timedelta

# Replace 'YOUR_API_KEY' with your actual Riot Games API key
API_KEY = 'RGAPI-1d8bdaef-ca6e-476d-9a0a-9d22bb8beb23'

map_server_to_region = {
    # "The AMERICAS routing value serves NA, BR, LAN and LAS. 
    # The ASIA routing value serves KR and JP. 
    # The EUROPE routing value serves EUNE, EUW, TR and RU. 
    # The SEA routing value serves OCE, PH2, SG2, TH2, TW2 and VN2."- https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID

    "NA1" : "AMERICAS",
    "BR1" : "AMERICAS",
    "LA1" : "AMERICAS",
    "LA2" : "AMERICAS",

    "KR" : "ASIA",
    "JP1" : "ASIA",

    "EUW1" : "EUROPE",
    "EUN1" : "EUROPE",
    "TR1" : "EUROPE",
    "RU" : "EUROPE",

    "OC1" : "SEA",
    "PH2" : "SEA",
    "SG2" : "SEA",
    "TH2" : "SEA",
    "TW2" : "SEA",
    "VN2" : "SEA",
}

def get_summoner_id(summoner_name, server):
    server = server.lower()
    url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        summoner_info = response.json()
        print(f"summoner ID: {summoner_info}")
        return summoner_info['puuid']
    else:
        print(f"Error getting summoner ID: {response.status_code}")

        return None

def get_matches_by_summoner(summoner_puuid, server, time_in_hours):

    params = {
        'api_key': API_KEY,
         #epoch time in seconds, from now minus 24 hours
        'startTime' : int((datetime.utcnow() - timedelta(hours=time_in_hours)).timestamp()),
        'endTime' : int(datetime.utcnow().timestamp() ),
    }

    region = map_server_to_region[server]

    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids"
    try:
        response = requests.get(api_url, params=(params))
        response.raise_for_status()
        print(response.json())

        #return length of the list of the match ids in past 24
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner match data from API: {e}')
        return None
    
def get_number_of_games_today(summoner_name, server):
    summoner_id = get_summoner_id(summoner_name, server)
    if summoner_id:
        ONE_DAY =  24
        games_today = len(get_matches_by_summoner(summoner_id, server, ONE_DAY))
        print(f"{summoner_name} has played {games_today} games today.")
        return games_today
    else:
        print("Error retrieving summoner ID.")
        #return infinity
        return 0