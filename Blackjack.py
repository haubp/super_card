from CardsBox import *
import arcade


class Blackjack:
    def __init__(self):
        self.players = arcade.SpriteList()
        self.cardsBox = CardsBox()
        self.turn = 0
        self.done = False
        self.result = ""

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
        if not self.done:
            self.cardsBox.draw()
        if self.result != "":
            arcade.draw_text(self.result, 350, 300, arcade.color.WHITE, 14)

    def update(self):
        for player in self.players:
            player.update()

    def on_mouse_press(self, x, y):
        if self.cardsBox.collides_with_point((x, y)):
            self.distribute_card(self.players[self.turn % len(self.players)])
            self.turn += 1
            self.cardsBox.on_click()

    def on_mouse_release(self, x, y):
        self.cardsBox.reset()
        winners, losers = self.check_game_logic()
        if len(losers) == len(self.players) or len(winners) == len(self.players):
            self.result = "Draw"
        elif len(winners) > 0:
            for index, p in enumerate(winners):
                self.result = f"{p.name} is the winner"
        elif len(losers) > 0:
            for index, p in enumerate(losers):
                self.result = f"{p.name} is the loser"

    def add_player(self, player):
        self.players.append(player)

    def distribute_card_for_all(self):
        for i in range(2):
            for p in self.players:
                p.add_card(self.cardsBox.get_card())

    def distribute_card(self, p):
        p.add_card(self.cardsBox.get_card())

    def check_game_logic(self):
        highest_point = 0
        winners = []
        losers = []
        for p in self.players:
            total_point = p.get_cards_point()
            if 15 < total_point < 22 and total_point >= highest_point:
                highest_point = total_point
            if total_point > 21:
                self.done = True
                losers.append(p)
        for p in self.players:
            if p.get_cards_point() == highest_point:
                self.done = True
                winners.append(p)
        return winners, losers
