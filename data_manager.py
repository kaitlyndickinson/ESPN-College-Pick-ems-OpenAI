import requests
import constants


# https://api.collegefootballdata.com/api/docs/?url=/api-docs.json
class DataManager:
    """
    Class to interact with the College Football Data API. 
    Fetching games, getting records, and win-loss ratios.
    """
    def __init__(self, week):
        self.headers = {
            "Authorization": f"Bearer {constants.API_KEY}",
        }

        self.games = 0
        self.week = week

    def get_current_week(self, team):
        """
        Gets details of the games played by the given team during a specified week.
        Uses the /games endpoint.
        """
        # TODO: set year in init
        params = {
            "year": 2024,
            "week": self.week,
            "seasonType": "regular",
            "division": "fbs",
            "team": team,
        }

        response = requests.get(
            "https://api.collegefootballdata.com/games",
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            games = response.json()
            formatted_games = "\n".join(
                [
                    f"{game['homeTeam']} vs {game['awayTeam']}, "
                    f"Week: {game.get('week')}, "
                    f"Venue: {game.get('venue')}, "
                    f"Neutral Site: {game.get('neutralSite')}, "
                    f"Conference Game: {game.get('conferenceGame')}, "
                    f"Home Team Conference: {game.get('homeConference')}, "
                    f"Home Team Division: {game.get('homeDivision')}, "
                    f"Away Team Conference: {game.get('awayConference')}, "
                    f"Away Team Division: {game.get('awayDivision')}, "
                    f"Home Team Points: {game.get('homePoints')}, "
                    f"Away Team Points: {game.get('awayPoints')}, "
                    f"Home Team Elo (Pregame): {game.get('homePregameElo')}, "
                    f"Home Team Elo (Postgame): {game.get('homePostgameElo')}, "
                    f"Away Team Elo (Pregame): {game.get('awayPregameElo')}, "
                    f"Away Team Elo (Postgame): {game.get('awayPostgameElo')}, "
                    f"Home Team Win Probability: {game.get('homePostgameWinProbability')}, "
                    f"Away Team Win Probability: {game.get('awayPostgameWinProbability')}"
                    for game in games
                ]
            )

        return formatted_games, games[0]["homeTeam"], games[0]["awayTeam"]

    def get_previous_week(self, team):
        """
        Gets details of the games played by the given team during a specified week.
        This function is different than get_current_week because less data is returned.
        E.g. we don't need ALL this data every single week (and it will overload the LLM) .
        Uses the /games endpoint.
        """
        # TODO: set year in init
        params = {
            "year": 2024,
            "week": self.week,
            "seasonType": "regular",
            "division": "fbs",
            "team": team,
        }

        response = requests.get(
            "https://api.collegefootballdata.com/games",
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            live_games = response.json()

            formatted_week = f"\nWeek {self.week}\n"
            formatted_week += "\n".join(
                [
                    f"{game['homeTeam']} vs {game['awayTeam']}, "
                    f"Venue: {game.get('venue')}, "
                    f"Neutral Site: {game.get('neutralSite')}, "
                    f"Conference Game: {game.get('conferenceGame')}, "
                    f"Score: {game['homeTeam']} {game['homePoints']} - {game['awayPoints']} {game['awayTeam']}, "
                    f"Home Elo: {game['homePregameElo']} -> {game['homePostgameElo']}, "
                    f"Away Elo: {game['awayPregameElo']} -> {game['awayPostgameElo']}, "
                    f"Home Win Probability: {game['homePostgameWinProbability']}, "
                    f"Away Win Probability: {game['awayPostgameWinProbability']}, "
                    f"Home Conference: {game.get('homeConference')}, "
                    f"Home Division: {game.get('homeDivision')}, "
                    f"Away Conference: {game.get('awayConference')}, "
                    f"Away Division: {game.get('awayDivision')}"
                    for game in live_games
                ]
            )
            return formatted_week
        else:
            return f"\nTeam {team} did not play any games week {self.week}\n"

    def win_loss_ratio(self, teams):
        """
        Computes the win-loss ratio for a list of teams, using the /records endpoint.
        """
        team_win_loss_map = {}

        for team in teams:
            params = {
                "year": 2024,
                "team": team,
            }

            response = requests.get(
                "https://api.collegefootballdata.com/records",
                headers=self.headers,
                params=params,
            )

            if response.status_code == 200:
                team_records = response.json()
                if team_records:
                    record = team_records[
                        0
                    ]  # There should only be one record per team (I assume)
                    team_win_loss_map[team] = (
                        f"{record['total']['wins']}-{record['total']['losses']}"
                    )
                else:
                    team_win_loss_map[team] = (
                        "No record available"  # This means, they (hopefully) haven't played yet?? Seems that the API doesn't list stats for teams that haven't played so far.
                    )
            else:
                team_win_loss_map[team] = "API error?"

        formatted_ratios = "\n".join(
            [f"{team}: {record}" for team, record in team_win_loss_map.items()]
        )

        return formatted_ratios

    def get_team_records(self, team):
        """
        Gets records for a specific team, using the /records endpoint.
        """
        params = {
            "year": 2024,
            "seasonType": "regular",
            "team": team,
        }

        response = requests.get(
            "https://api.collegefootballdata.com/records",
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            records = response.json()
            return (
                f"Team: {records[0]['team']}\n"
                f"Conference: {records[0]['conference']}\n"
                f"Wins: {records[0]['total']['wins']}, Losses: {records[0]['total']['losses']}, Ties: {records[0]['total']['ties']}"
            )
        else:
            return f"No data available for team {team}."