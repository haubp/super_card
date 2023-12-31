from Blackjack import *
from Player import *
from GameBoard import *
import arcade


def main():
    blackjack_game = Blackjack()

    p1 = Player(True, "me", "hau", "./assets/man.png", SPRITE_SCALING_PLAYER)
    p2 = Player(False, "other", "nguyen", "./assets/man.png", SPRITE_SCALING_PLAYER)
    p3 = Player(False, "other", "nam", "./assets/man.png", SPRITE_SCALING_PLAYER)
    p4 = Player(False, "other", "thien", "./assets/man.png", SPRITE_SCALING_PLAYER)

    blackjack_game.add_player(p1)
    blackjack_game.add_player(p2)
    blackjack_game.add_player(p3)
    blackjack_game.add_player(p4)

    board = GameBoard(blackjack_game)

    board.setup()
    arcade.run()


if __name__ == "__main__":
    main()
