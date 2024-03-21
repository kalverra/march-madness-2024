import csv
import random

def read_csv_to_dict(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

filename = 'March_Madness_2024_Silver_Bulletin_03_19_2024.csv'
data = read_csv_to_dict(filename)

east = []
west = []
south = []
midwest = []

for row in data:
    if row['team_region'] == 'East':
        east.append(row)
    elif row['team_region'] == 'West':
        west.append(row)
    elif row['team_region'] == 'South':
        south.append(row)
    elif row['team_region'] == 'Midwest':
        midwest.append(row)

regions = [east, west, south, midwest]

def print_region(region:str):
    region_str = ""
    for team in region:
        region_str += team['team_name'] + ", "
    print(region_str)
    print()

def simulate(upset_biased:bool = False):
    global regions
    upset_count = 0
    rounds = 8
    for round in range(2, rounds):
        if round == 6:
            combined_regions = []
            for region in regions:
                region[0]["team_region"] = "Final Four"
                combined_regions.append(region[0])
            regions = [combined_regions]
        if round == 7:
            regions[0][0]["team_region"] = "Championship"
            
        print("=============")
        print(f'Round {round}')
        print("=============")
        print()
        for region_index, region in enumerate(regions):
            print("-----------")
            print(region[0]['team_region'])
            print("-----------")
            new_region = []
            for i in range(0, len(region), 2):
                team1 = region[i]
                team2 = region[i + 1]
                rd_string = f"rd{round}_win"
                higher_rated_team = team1 if float(team1[rd_string]) > float(team2[rd_string]) else team2
                lower_rated_team = team1 if float(team1[rd_string]) <= float(team2[rd_string]) else team2
                higher_rated_score = float(team1[rd_string]) if float(team1[rd_string]) > float(team2[rd_string]) else float(team2[rd_string])
                lower_rated_score = float(team1[rd_string]) if float(team1[rd_string]) <= float(team2[rd_string]) else float(team2[rd_string])
                to_beat = higher_rated_score - (lower_rated_score / 2)
                roll = random.uniform(0, higher_rated_score)
                winner = None
                upset = False
                if upset_biased:
                    roll *= 1.25

                if roll >= to_beat:
                    winner = lower_rated_team
                    upset = True
                    upset_count += 1
                else:
                    winner = higher_rated_team
                new_region.append(winner)
                print(f'{higher_rated_team["team_name"]:<21} @ {higher_rated_score:<7.3} vs {lower_rated_team["team_name"]:<21} @ {lower_rated_score:<7.3}: Rolled {roll:<7.3} to beat {to_beat:<7.3} => {winner["team_name"]:<21} Upset? {upset}')
            regions[region_index] = new_region
            print()
    print()
    print(f"Upset Count: {upset_count}")

simulate(True)
