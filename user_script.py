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
            "year": 2024,
            "week": week,
            "seasonType": "regular",
            "division": "fbs",
        }
     response = requests.get(url, headers=headers, params=params)

     if response.status_code == 200:
            games = response.json()

            with open(f"2024_w{week}.json", 'w') as json_file:
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

    rows = resp.json() or []
    payload = {"team": team, "year": year, "raw": rows}

    if rows:
        r0 = rows[0]
        payload["summary"] = {
            "overall": {"rating": r0.get("rating"), "rank": r0.get("ranking")},
            "offense": {"rating": r0.get("offense"), "rank": r0.get("offenseRank")},
            "defense": {"rating": r0.get("defense"), "rank": r0.get("defenseRank")},
        }

    filename = f"{team}_{year}_offense_defense_scores.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--export", type=str)
    parser.add_argument("-c", "--count", type=str)
    parser.add_argument("-s", "--score", type=str)

    args = parser.parse_args()

    if args.export:
        export_week(args.export)
    if args.count:
        get_total_results(args.count)
    if args.score:
         export_team_scores(args.score)
         
if __name__ == "__main__":
    main()