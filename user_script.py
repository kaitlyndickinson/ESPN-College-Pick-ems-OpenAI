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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--export", type=str)
    parser.add_argument("-c", "--count", type=str)

    args = parser.parse_args()

    if args.export:
        export_week(args.export)
    if args.count:
        get_total_results(args.count)

if __name__ == "__main__":
    main()
