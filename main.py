
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

@dataclass
class Round:
    level: str
    position: int
    best: int
    avg: int
    format: str
    solves: list[int]

@dataclass
class Event:
    name: str
    rounds: list[Round]

@dataclass
class Competition:
    name: str
    events: list[Event]

def get_basic_info(json_obj):
    id = json_obj["id"]
    name = json_obj["name"]
    country = json_obj["country"]
    num_comps = json_obj["numberOfCompetitions"]
    return id, name, country, num_comps

def get_attended_comps(json_obj, type):
    comps_json = json_obj[type]
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

def get_results(json_obj):
    results = json_obj["results"]
    for key, value in results.items():
        comp = Competition("", [])
        comp.name = key
        events = []
        for event_key, event_list in value.items():
            event = Event("", [])
            event.name = event_key
            for event_val in event_list:
                round = Round("", 0, 0, 0, "", [])
                round.level = event_val["round"]
                round.position = event_val["position"]
                round.best = event_val["best"]
                round.average = event_val["average"]
                round.format = event_val["format"]
                round.solves = event_val["solves"]
                event.rounds.append(round)
            events.append(event)
        comp.events.append(events)

    return comp
            

def main():
    user_id = sys.argv[1]
    response = requests.get("https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/refs/heads/v1/persons/"+user_id+".json")
    response_json = response.json()
    # id, name, country, num_comps = get_basic_info(response_json)
    # comps = get_attended_comps(response_json)
    # ranks_avg = get_rankings(response_json, "averages")
    # rank_three = get_event_rankings(ranks_avg, "333")
    # print("PR = ",rank_three.best)
    # print("WR = ",rank_three.world)
    # print("CR = ",rank_three.continent)
    # print("NR = ",rank_three.country)
    comp = get_results(response_json)
    print("COMP NAME:"+comp.name)
    event = comp.events[0]
    for e in event:
        print("EVENT:"+e.name)
        for round in e.rounds:
            print("\tROUND:"+round.level)
            print("\tROUND RANK:",round.position)
            print("\tAVERAGE:",round.average) if round.average != 1 else print("\tAVERAGE: DNF")
            print("\tBEST SINGLE:",round.best)
            print("\tFORMAT:"+round.format)
            iter = 1
            for time in round.solves:
                if(time != 0):
                    print("\t",iter,". ",time, sep="")
                else:
                    break
                iter += 1
            
    
    # response_json = json.dumps(response_json, indent=4)
    # print(response_json)
    

if __name__ ==  "__main__":
    main()
