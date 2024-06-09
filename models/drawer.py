from .utils import extract_content


class Drawer:
    def __init__(self, client, game_rules, model="gpt-3.5-turbo"):
        self.client = client
        self.model = model
        self.messages = [
            {"role": "system", "content": f"There is a game with these rules: {game_rules}. " + 
                                           "you are only allowed to draw the actual game state after the player move "},
        ]
    
    def draw(self, move):
        return extract_content(self.client.chat.completions.create(
            model = self.model,
            messages = self.messages + [{"role": "user", "content": f"This is my move {move}"}],
            temperature = 0.1
        ))