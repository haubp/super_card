from CardsBox import *
from TextInput import *
from Button import *
import arcade


class Blackjack:
    def __init__(self):
        self.players = arcade.SpriteList()
        self.cardsBox = CardsBox()
        self.bidInput = TextInput(150, 50, 100, 30)
        self.startButton = Button(400, 300, 100, 50, "Start")
        self.turn = 1
        self.time = 0
        self.state = "BET"

    def setup(self):
        if len(self.players) == 4:
            self.players[0].center_x = 400
            self.players[0].center_y = 50
            self.players[1].center_x = 200
            self.players[1].center_y = 550
            self.players[2].center_x = 400
            self.players[2].center_y = 550
            self.players[3].center_x = 600
            self.players[3].center_y = 550

        self.cardsBox.center_x = 400
        self.cardsBox.center_y = 300

        self.distribute_card_for_all()

    def draw(self):
        if self.state == "BET":
            self.startButton.draw()
        elif self.state == "PLAY":
            for player in self.players:
                player.draw()
            self.cardsBox.draw()
            self.bidInput.draw()


    def update(self):
        if self.state == "PLAY":
            self.time += 1
            if self.time == 300:
                self.time = 0
                self.players[self.turn % len(self.players)].is_distributed = True
                self.turn += 1

            for index, player in enumerate(self.players):
                player.update()

            self.players[self.turn % len(self.players)].time = self.time / 60

    def on_mouse_press(self, x, y):
        if self.cardsBox.collides_with_point((x, y)) and not self.players[self.turn % len(self.players)].is_distributed:
            card = self.cardsBox.get_card()
            if self.players[self.turn % len(self.players)].role == "me":
                card.up()
                self.players[self.turn % len(self.players)].add_card(card)
            else:
                card.down()
                self.players[self.turn % len(self.players)].add_card(card)
            self.cardsBox.on_click()
        for player in self.players:
            if player.collides_with_point((x, y)) and player.role != "me" and player.is_distributed:
                for card in player.cards:
                    card.up()
        self.bidInput.on_mouse_press(x, y)

    def on_mouse_release(self, x, y):
        self.cardsBox.reset()
        self.startButton.on_mouse_release(x, y)
        if self.startButton.is_pressed:
            self.startButton.is_pressed = False
            self.state = "PLAY"

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.startButton.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        self.bidInput.on_key_press(symbol, modifiers)

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

