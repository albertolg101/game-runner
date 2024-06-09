from openai import OpenAI
from models import Validator, Player, GameStateDecider, Drawer
from dotenv import load_dotenv
from os import getenv

def main():
    load_dotenv()
    RULES = getenv('RULES')

    client = OpenAI()

    validator = Validator(client, RULES)
    actual_player = Player(client, validator,'Player 1', RULES)
    other_player = Player(client, validator, 'Player 2', RULES)
    game_state_decider = GameStateDecider(client, RULES)
    drawer = Drawer(client, RULES)

    while(True):
        move = actual_player.play()
        game_state = game_state_decider.decide(move)
        game_state_draw = drawer.draw(move)

        print(f"------------ {actual_player.name} ------------")
        print(game_state_draw)
        print("------------- STATE --------------")
        print(game_state)
        print("----------------------------------")
        input("Press enter to continue")
        print("\n\n\n")

        actual_player.messages.append({"role": "user", "content": "explain your next move as simple as possible"})
        actual_player.messages.append({"role": "user", "content": move})
        other_player.messages.append({"role": "user", "content": f"The other player played {move}"})
        other_player.messages.append({"role": "user", "content": f"This is the actual game state {game_state_draw}"})
        validator.messages.append({"role": "user", "content": game_state_draw})
        validator.messages.append({"role": "assistant", "content": "yes"})
        drawer.messages.append({"role": "user", "content": move})
        drawer.messages.append({"role": "assistant", "content": game_state_draw})
        actual_player, other_player = other_player, actual_player


if __name == "__main__":
    main()