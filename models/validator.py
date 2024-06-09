from .utils import extract_content


class Validator:
    def __init__(self, client, game_rules, model="gpt-3.5-turbo"):
        self.client = client
        self.model = model
        self.messages = [
            {"role": "system", "content": f"You will be the validator for a game with these rules: {game_rules} "
                                            "You will only return 'yes' if the movement is valid."},
        ]
    
    def validate(self, move):
        validation = self.client.chat.completions.create(
            model = self.model,
            messages = self.messages + [{"role": "user", "content": move}],
        )

        return (extract_content(validation).lower().find("yes") != -1)