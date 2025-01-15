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

    def get_results(self):
        """
        Generates predictions and explanations for this week's games using gpt-4o-mini. 
        Also formats the prompt.
        """
        prompt = self.format_prompt()

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
            model="gpt-4o-mini",
        )

        return completion.choices[0].message.content
    
    def format_prompt(self):
        """
        Formats the prompt with the game and team data to provide context.
        """
        PROMPT = f"""Given the college football game this week and the data provided, give a prediction on which team will end this week and what the final score will be. Give a short explaination as to why. 

        This week's game data:
        {self.current_week}

        Home team data:
        {self.home_records}

        Away team data:
        {self.away_records}

        Home team previous weeks performances:
        {self.home_games}\n

        Away team previous weeks performances:
        {self.away_games}\n
        """

        return PROMPT