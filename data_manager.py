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
            "year": 2025,
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

            if not games:
                # No game found for this team in the current week
                formatted_games = f"No game scheduled for {team} in week {self.week}."
                return formatted_games, None, None
        
            formatted_games = "\n".join(
                [
                    f"{game.get('homeTeam')} vs {game.get('awayTeam')}\n"
                    f"Week: {game.get('week')}\n"
                    f"Venue: {game.get('venue')}\n"
                    f"Neutral Site: {game.get('neutralSite')}\n"
                    f"Conference Game: {game.get('conferenceGame')}\n"
                    f"Home Team Conference: {game.get('homeConference')}\n"
                    f"Home Team Division: {game.get('homeDivision')}\n"
                    f"Away Team Conference: {game.get('awayConference')}\n"
                    f"Away Team Division: {game.get('awayDivision')}\n"
                    f"Home Team Elo (Pregame): {game.get('homePregameElo')}\n"
                    f"Home Team Elo (Postgame): {game.get('homePostgameElo')}\n"
                    f"Away Team Elo (Pregame): {game.get('awayPregameElo')}\n"
                    f"Away Team Elo (Postgame): {game.get('awayPostgameElo')}\n"
                    f"Home Team Win Probability: {game.get('homePostgameWinProbability')}\n"
                    f"Away Team Win Probability: {game.get('awayPostgameWinProbability')}"
                    for game in games
                ]
            )

            # Return only the first game details, as we assume one game per week for a team
            return formatted_games, games[0]["homeTeam"], games[0]["awayTeam"]
        
        error_msg = f"No data for {team} in week {self.week} — Status code: {response.status_code}"
        return error_msg, None, None


    def get_previous_weeks(self, team):
        """
        Gets summary scores of the games played by the given team in all weeks prior to the current one.
        """
        params = {
            "year": 2025,
            "seasonType": "regular",
            "division": "fbs",
            "team": team,
        }

        response = requests.get(
            "https://api.collegefootballdata.com/games",
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            return f"Failed to retrieve games for {team}. Status code: {response.status_code}"

        all_games = response.json()

        # Filter out games that are after or during the current week
        past_games = [
            game for game in all_games
            if game.get("week") is not None and game["week"] < self.week
        ]

        if not past_games:
            return f"No previous games found for {team} before week {self.week}.\n"

        output = []
        for game in past_games:
            week = game["week"]
            home = game["homeTeam"]
            away = game["awayTeam"]
            home_pts = game["homePoints"]
            away_pts = game["awayPoints"]

            line = f"Week {week}: {home} {home_pts} - {away} {away_pts}"
            output.append(line)

        return "\n".join(output) if output else f"No data for {team} before week {self.week}.\n"


    def win_loss_ratio(self, teams):
        """
        Computes the win-loss ratio for a list of teams, using the /records endpoint.
        """
        team_win_loss_map = {}

        for team in teams:
            params = {
                "year": 2025,
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
            "year": 2025,
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
            
            if records:
                return (
                    f"Team: {records[0]['team']}\n"
                    f"Conference: {records[0]['conference']}\n"
                    f"Wins: {records[0]['total']['wins']}, Losses: {records[0]['total']['losses']}, Ties: {records[0]['total']['ties']}"
                )
            else:
                return f"This is likely a team that hasn't played yet this season: {team}."
        else:
            return f"No data available for team {team}." 
