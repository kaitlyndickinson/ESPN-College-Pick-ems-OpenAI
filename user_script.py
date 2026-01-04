import argparse
import json
import requests
import constants

headers = {
    "Authorization": f"Bearer {constants.API_KEY}",
}

url = "https://api.collegefootballdata.com/games"


# Just some functions to help with testing, need to clean up.
def export_week(week):
    params = {
        "year": 2025,
        "week": week,
        "seasonType": "regular",
        "division": "fbs",
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        games = response.json()

        with open(f"2025_w{week}.json", "w") as json_file:
            json.dump(games, json_file, indent=4)


def get_total_results(week):
    params = {
        "year": 2024,
        "week": week,
        "seasonType": "regular",
        "division": "fbs",
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        games = response.json()

        print(len(games))
    else:
        print("Unsuccessful.")


def export_team_scores(team, year=2025):
    sp_url = "https://api.collegefootballdata.com/ratings/sp"
    params = {"year": year, "team": team}
    resp = requests.get(sp_url, headers=headers, params=params)

    if resp.status_code != 200:
        print("Failed to fetch SP+:", resp.text)
        return

    sp = resp.json()

    formatted_games = "\n".join(
        [
            "SP+ Metrics:\n"
            f"Overall Ranking: {sp[0]['ranking']}\n"
            f"Overall Rating: {sp[0]['rating']}\n"
            f"Offense Ranking: {sp[0]['offense']['ranking']}\n"
            f"Offense Rating: {sp[0]['offense']['rating']}\n"
            f"Defense Ranking: {sp[0]['defense']['ranking']}\n"
            f"Defnse Rating: {sp[0]['defense']['rating']}\n"
        ]
    )
    print(formatted_games)

def get_roster(team, year=2025):
    url = "https://api.collegefootballdata.com/roster"
    params = {"year": year, "team": team}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    with open(f"2025_roster.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def get_player_stats(team, year=2025):
    url = "https://api.collegefootballdata.com/stats/player/season"
    params = {"year": year, "team": team}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    for entry in data:
        print(entry['position'])

    

    # if resp.status_code != 200:
    #     print("Failed to fetch player data:", resp.text)
    #     return

    # data = resp.json()
    # with open("2025_player.json", "w") as json_file:
    #     json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--export", type=str)
    parser.add_argument("-c", "--count", type=str)
    parser.add_argument("-s", "--score", type=str)
    parser.add_argument("-p", "--player", type=str)
    parser.add_argument("-r", "--roster", type=str)

    args = parser.parse_args()

    if args.export:
        export_week(args.export)
    if args.count:
        get_total_results(args.count)
    if args.score:
        export_team_scores(args.score)
    if args.player:
        get_player_stats(args.player)
    if args.roster:
        get_roster(args.roster)

if __name__ == "__main__":
    main()
