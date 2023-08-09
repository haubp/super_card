from CardsBox import *
from TextInput import *
from Button import *
import arcade


class Blackjack:
    def __init__(self):
        self.players = arcade.SpriteList()
        self.cardsBox = None
        self.bidInput = TextInput(450, 300, 100, 30)
        self.betButton = Button(550, 300, 100, 50, "Bet")
        self.startButton = Button(450, 300, 100, 50, "Start")
        self.restartButton = Button(450, 300, 100, 50, "Again")
        self.turn = 1
        self.time = 0
        self.state = "START"
        self.myselfIndex = 0
        self.finished_player = 0

    def setup(self):
        if len(self.players) == 4:
            self.players[0].center_x = 400
            self.players[0].center_y = 50
            self.players[1].center_x = 150
            self.players[1].center_y = 550
            self.players[2].center_x = 400
            self.players[2].center_y = 550
            self.players[3].center_x = 650
            self.players[3].center_y = 550

        self.cardsBox = CardsBox()
        self.cardsBox.center_x = 400
        self.cardsBox.center_y = 300

        self.turn = 1
        self.time = 0
        self.finished_player = 0

        for player in self.players:
            player.cards.clear()
            player.is_distributed = False
            player.time = 0

        self.distribute_card_for_all()

    def draw(self):
        if self.state == "START":
            self.startButton.draw()
        elif self.state == "BET":
            self.bidInput.draw()
            self.betButton.draw()
        elif self.state == "PLAY":
            for player in self.players:
                player.draw()
            self.cardsBox.draw()
        elif self.state == "FINISH":
            for player in self.players:
                player.draw()
            self.restartButton.draw()

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
        if self.state == "PLAY":
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
                if player.collides_with_point((x, y)) and \
                        player.role != "me" and \
                        player.is_distributed:
                    for card in player.cards:
                        card.up()
                    self.calculate_cards_point(player)
                    self.finished_player += 1
                    if self.finished_player == 3:
                        self.state = "FINISH"
        elif self.state == "BET":
            self.bidInput.on_mouse_press(x, y)

    def on_mouse_release(self, x, y):
        if self.state == "PLAY":
            self.cardsBox.reset()
        elif self.state == "START":
            self.startButton.on_mouse_release(x, y)
            if self.startButton.is_pressed:
                self.startButton.is_pressed = False
                self.startButton.is_hovered = False
                self.state = "BET"
        elif self.state == "FINISH":
            self.restartButton.on_mouse_release(x, y)
            if self.restartButton.is_pressed:
                self.restartButton.is_pressed = False
                self.restartButton.is_hovered = False
                self.cardsBox = None
                self.state = "BET"
                self.setup()
        elif self.state == "BET":
            self.betButton.on_mouse_release(x, y)
            if self.betButton.is_pressed:
                self.players[self.myselfIndex].bet(self.bidInput.text)
                self.betButton.is_pressed = False
                self.betButton.is_hovered = False
                self.state = "PLAY"

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.state == "START":
            self.startButton.on_mouse_motion(x, y, dx, dy)
        elif self.state == "FINISH":
            self.restartButton.on_mouse_motion(x, y, dx, dy)
        elif self.state == "BET":
            self.betButton.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == "BET":
            self.bidInput.on_key_press(symbol, modifiers)
            if self.bidInput.is_entered:
                self.players[self.myselfIndex].bet(self.bidInput.text)
                self.state = "PLAY"
                self.bidInput.is_entered = False

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

    def calculate_cards_point(self, player):
        my_point = self.players[self.myselfIndex].get_cards_point()
        opponent_point = player.get_cards_point()
        if 14 <= my_point <= 21 and 14 <= opponent_point <= 21:
            if my_point > opponent_point:
                self.players[self.myselfIndex].balance += player.bid
                player.balance -= player.bid
            elif my_point < opponent_point:
                self.players[self.myselfIndex].balance -= player.bid
                player.balance += player.bid
        elif 14 <= my_point <= 21:
            self.players[self.myselfIndex].balance += player.bid
            player.balance -= player.bid
        elif 14 <= opponent_point <= 21:
            self.players[self.myselfIndex].balance -= player.bid
            player.balance += player.bid
