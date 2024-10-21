' ' 'Sorts players into arrays by position' ' '

# Imports
import json
import statistics

# Parameters
teams = 10
budget = 250
roster = 13
pg_spot = 1
sg_spot = 1
sf_spot = 1
pf_spot = 1
center_spot = 1
guard_spot = 1
forward_spot = 1
utility_spot = 3
bench_spot = 3
# below calc assumes all bench players are worth $1
starter_budget = budget * teams - bench_spot * teams

# Open JSON file and parse as JSON into players list
with open('data.json', encoding="utf-8") as file:
    players = json.load(file)
    draftable_players = players[:(teams*roster)]

# Create lists for each position
pguard = []
sguard = []
sforward = []
pforward = []
center = []
guard = []
forward = []
utility = []

for points in draftable_players:
    points["Points"] = round(points["Points"])

# Loop through all players and add to lists based on position
for player in draftable_players:
    for position in player["Positions"]:
        match position:
            case "PG":
                pguard.append(player)
                if player not in guard:
                    guard.append(player)
                if player not in utility:
                    utility.append(player)
            case "SG":
                sguard.append(player)
                if player not in guard:
                    guard.append(player)
                if player not in utility:
                    utility.append(player)
            case "SF":
                sforward.append(player)
                if player not in forward:
                    forward.append(player)
                if player not in utility:
                    utility.append(player)
            case "PF":
                pforward.append(player)
                if player not in forward:
                    forward.append(player)
                if player not in utility:
                    utility.append(player)
            case "C":
                center.append(player)
                if player not in utility:
                    utility.append(player)

#optimal starter totals
total_starters = teams * roster - bench_spot * teams
startable_players = utility[:total_starters]

startable_pg = []
startable_sg = []
startable_sf = []
startable_pf = []
startable_c = []
startable_g = []
startable_f = []
startable_util = []

for player in startable_players:
    for position in player["Positions"]:
        match position:
            case "PG":
                startable_pg.append(player)
                if player not in startable_g:
                    startable_g.append(player)
                if player not in startable_util:
                    startable_util.append(player)
            case "SG":
                startable_sg.append(player)
                if player not in startable_g:
                    startable_g.append(player)
                if player not in startable_util:
                    startable_util.append(player)
            case "SF":
                startable_sf.append(player)
                if player not in startable_f:
                    startable_f.append(player)
                if player not in startable_util:
                    startable_util.append(player)
            case "PF":
                startable_pf.append(player)
                if player not in startable_f:
                    startable_f.append(player)
                if player not in startable_util:
                    startable_util.append(player)
            case "C":
                startable_c.append(player)
                if player not in startable_util:
                    startable_util.append(player)

worst_pg = startable_pg[-1]
worst_pg_pts = worst_pg["Points"]
worst_sg = startable_sg[-1]
worst_sg_pts = worst_sg["Points"]
worst_sf = startable_sf[-1]
worst_sf_pts = worst_sf["Points"]
worst_pf = startable_pf[-1]
worst_pf_pts = worst_pf["Points"]
worst_c = startable_c[-1]
worst_c_pts = worst_c["Points"]
worst_g = startable_g[-1]

for player in startable_util:
    if player in startable_pg:
        if player in startable_sg:
            player["Points"] = ((player["Points"] - worst_pg_pts) + ((player["Points"]) - worst_sg_pts))/2
        else:
            player["Points"] -= worst_pg_pts
    if player in startable_sg:
        if player in startable_pg:
            pass
        elif player in startable_sf:
            player["Points"] = ((player["Points"] - worst_sg_pts) + ((player["Points"]) - worst_sf_pts))/2
        else:
            player["Points"] -= worst_sg_pts
    if player in startable_sf:
        if player in startable_sg:
            pass
        elif player in startable_pf:
            player["Points"] = ((player["Points"] - worst_sf_pts) + ((player["Points"]) - worst_pf_pts))/2
        else:
            player["Points"] -= worst_sf_pts
    if player in startable_pf:
        if player in startable_sf:
            pass
        elif player in startable_c:
            player["Points"] = ((player["Points"] - worst_pf_pts) + ((player["Points"]) - worst_c_pts))/2
        else:
            player["Points"] -= worst_pf_pts
    if player in startable_c:
        if player in startable_pf:
            pass
        else:
            player["Points"] -= worst_c_pts
  
points_above_min = []  
      
for player in startable_util:
    points_above_min.append(player["Points"])
    
total_points_above_min = sum(points_above_min)     

dollar_per_point = starter_budget / total_points_above_min

sorted_ranks = sorted(startable_util, key=lambda x: x["Points"], reverse = True)

# for player in sorted_ranks:
#     print("$",round(player["Points"]*dollar_per_point), " - ", player["NAME"])

with open("output.csv", "w") as f:
    for player in sorted_ranks:
        print(f"${round(player["Points"] * dollar_per_point)},{player["NAME"]}", file = f)