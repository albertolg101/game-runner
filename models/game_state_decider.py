from .utils import extract_content


class GameStateDecider:
    def __init__(self, client, game_rules, model="gpt-3.5-turbo"):
        self.client = client
        self.model = model
        self.game_rules = game_rules
        self.messages = [
            {"role": "system", "content": f"You task is to say when a game is over"},
            {"role": "user", "content": f"Given this rules {game_rules} and the next set of movements "}
        ]

    def decide(self, move):
        self.messages.append({"role": "user", "content": move})
        return extract_content(self.client.chat.completions.create(
            model = self.model,
            messages = self.messages + [{"role": "user", "content": f"This is the last state of the game {move} " + 
                                                                        "Is there a winner or the game continues? " + 
                                                                        "Do not justify answer"}],
            temperature = 0.1
        ))