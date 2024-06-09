from .utils import extract_content


class Player: 
    def __init__(self, client, validator, name, game_rules, model="gpt-3.5-turbo"):
        self.client = client
        self.validator = validator
        self.name = name
        self.model = model
        self.game_rules = game_rules
        self.messages = [
            {"role": "system", "content": f"- You are playing a game with this rules: {game_rules}\n" +
                                          f"- You are {name}"
                                           "- You dont justify your answers\n" +
                                           "- You want to win"},
        ]
    
    def play(self):
        move_attempt_count = 0
        is_move_valid = False

        while(not is_move_valid):
            move = extract_content(self.client.chat.completions.create(
                model = self.model,
                messages = self.messages + [{"role": "user", "content": "explain your next move as simple as possible"}],
                temperature = 0.5,
            ))
            is_move_valid = self.validator.validate(move)

            move_attempt_count += 1
            if move_attempt_count == 10:
                raise PlayerWasNotAbleToPlayCorrectly
        
        return move

class PlayerWasNotAbleToPlayCorrectly(Exception):
    pass