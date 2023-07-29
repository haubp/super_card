from Blackjack import *
from Player import *
from GameBoard import *
import arcade


def main():
    blackjack_game = Blackjack()

    p1 = Player("Hau", "./assets/man.png", SPRITE_SCALING_PLAYER)
    p2 = Player("Nguyen", "./assets/man.png", SPRITE_SCALING_PLAYER)

    blackjack_game.add_player(p1)
    blackjack_game.add_player(p2)

    board = GameBoard(blackjack_game)

    board.setup()
    arcade.run()


if __name__ == "__main__":
    main()
