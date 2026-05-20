
import sys
import requests
# import json
from dataclasses import dataclass

@dataclass
class Rank:
    event: str
    best: int
    world: int
    continent: int
    country: int

def get_basic_info(json_obj):
    id = json_obj["id"]
    name = json_obj["name"]
    country = json_obj["country"]
    num_comps = json_obj["numberOfCompetitions"]
    return id, name, country, num_comps

def get_attended_comps(json_obj):
    comps_json = json_obj["competitionIds"]
    comps = []
    for comp in comps_json:
        comps.append(comp)
    return comps

def get_rankings(json_obj, type):
    ranks_all = json_obj["rank"]
    rankset = ranks_all[type]
    ranks = []
    for rank in rankset:
        stats = Rank("",0,0,0,0)
        scales = rank["rank"]
        stats.event = rank["eventId"]
        stats.best = rank["best"]
        stats.world = scales["world"]
        stats.continent = scales["continent"]
        stats.country = scales["country"]
        ranks.append(stats)
    return ranks

def get_event_rankings(rankings ,event):
    ranks = Rank("",0,0,0,0)
    for rank in rankings:
        if(rank.event == event):
            ranks = rank
            break
    return ranks   

def main():
    user_id = sys.argv[1]
    response = requests.get("https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/refs/heads/v1/persons/"+user_id+".json")
    response_json = response.json()
    id, name, country, num_comps = get_basic_info(response_json)
    # comps = get_attended_comps(response_json)
    ranks_avg = get_rankings(response_json, "averages")
    rank_three = get_event_rankings(ranks_avg, "333")
    print("PR = ",rank_three.best)
    print("WR = ",rank_three.world)
    print("CR = ",rank_three.continent)
    print("NR = ",rank_three.country)
    
    # response_json = json.dumps(response_raw, indent=4)
    # print(response_json)
    
    print()

if __name__ ==  "__main__":
    main()
