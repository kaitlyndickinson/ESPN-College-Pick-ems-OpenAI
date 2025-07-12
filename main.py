import argparse
from data_manager import DataManager
from llm import LLM
import sys

sys.stdout.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(
        description="Get football predictions from team data."
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the input CSV file with team names.",
    )
    parser.add_argument(
        "-w",
        "--week",
        type=int,
        required=True,
        help="The current week number to fetch data for.",
    )

    args = parser.parse_args()

    if args.week and args.file:
        data_manager = DataManager(args.week)

        with open(args.file, "r") as file:
            data = file.read()

        # Expect a list of teams comma separated values, where the team name matches that of the API
        teams = data.split(",")

        teams = [team.strip() for team in teams]

        predictions = []

        with open("results.txt", "w", encoding="utf-8") as outfile:
            # Process one team at a time (during testing, I found making multiple API calls to OpenAI is much more efficient than shoving all the data down its throat)
            for team in teams:
                current_week, home_team, away_team = data_manager.get_current_week(team)
                home_records = data_manager.get_team_records(home_team)
                away_records = data_manager.get_team_records(away_team)

                home_games = data_manager.get_previous_weeks(home_team)
                away_games = data_manager.get_previous_weeks(away_team)

                llm = LLM(current_week, home_records, away_records, home_games, away_games)

                prediction = llm.get_results()
                predictions.append(prediction)
                outfile.write(f"=========================================================\n{prediction}\n")


if __name__ == "__main__":
    main()
