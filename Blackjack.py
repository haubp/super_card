from CardsBox import *
import arcade


class Blackjack:
    def __init__(self):
        self.players = arcade.SpriteList()
        self.cardsBox = CardsBox()
        self.turn = 0
        self.state = "begin"

    def setup(self):
        if len(self.players) == 2:
            self.players[0].center_x = 400
            self.players[0].center_y = 50
            self.players[1].center_x = 400
            self.players[1].center_y = 550

        self.cardsBox.center_x = 400
        self.cardsBox.center_y = 300

        self.distribute_card_for_all()

    def draw(self):
        for player in self.players:
            player.draw()
        self.cardsBox.draw()

    def update(self):
        for player in self.players:
            player.update()

    def on_mouse_press(self, x, y):
        if self.cardsBox.collides_with_point((x, y)):
            card = self.cardsBox.get_card()
            if self.players[self.turn % len(self.players)].role == "me":
                card.up()
                self.players[self.turn % len(self.players)].add_card(card)
            else:
                card.down()
                self.players[self.turn % len(self.players)].add_card(card)
            self.turn += 1
            self.cardsBox.on_click()

    def on_mouse_release(self, x, y):
        self.cardsBox.reset()

    def add_player(self, player):
        self.players.append(player)

    def distribute_card_for_all(self):
        for i in range(2):
            for p in self.players:
                card = self.cardsBox.get_card()
                if p.role == "me":
                    card.up()
                    p.add_card(card)
                else:
                    card.down()
                    p.add_card(card)

    def distribute_card(self, p):
        p.add_card(self.cardsBox.get_card())

