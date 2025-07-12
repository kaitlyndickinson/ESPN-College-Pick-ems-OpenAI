from openai import OpenAI
import constants

class LLM:
    """
    LLM class to generate predictions for college football games.
    """
    def __init__(self, current_week, home_records, away_records, home_games, away_games):
        self.current_week = current_week
        self.home_records = home_records
        self.away_records = away_records
        self.home_games = home_games
        self.away_games = away_games
        self.client = OpenAI(api_key=constants.OPENAI_API_KEY)

        # Instructions for the LLM to generate predictions
        self.instructions = """You are a sports analyst. Given the college football game this week and the data provided, give a prediction on which team will end this week and what the final score will be. Give a short explaination as to why. Format the response as follows:

        Prediction: [Team Name] will win this week against [Team Name] with a score of [Team A Score - Team B Score].
        
        Explanation: [Short explanation of the prediction based on the data provided].
        """

    def get_results(self):
        """
        Generates predictions and explanations for this week's games using o4-mini. 
        Also formats the prompt.
        """
        data = self.format_data()

        # completion = self.client.responses.create(
        #     instructions=self.instructions,
        #     model="o4-mini",
        #     input=data
        # )

        # return completion.output_text
        return data
    
    def format_data(self):
        """
        Formats the prompt with the game and team data to provide context.
        """
        DATA = f"""This week's game data: 
{self.current_week}
        
Home team data: 
{self.home_records}

Away team data:
{self.away_records}

Home team previous weeks performances:
{self.home_games}

Away team previous weeks performances:
{self.away_games}
"""
        
        return DATA