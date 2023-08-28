from CardsBox import *
from ChatBox import *
import arcade


class Blackjack:
    def __init__(self):
        self.players = arcade.SpriteList()
        self.cardsBox = None
        self.bidInput = TextInput(450, 300, 100, 30)
        self.betButton = Button(550, 300, 100, 50, "Bet")
        self.userNameInput = TextInput(450, 300, 100, 30)
        self.userName = ""
        self.loginButton = Button(550, 300, 100, 50, "Login")
        self.startButton = Button(450, 300, 100, 50, "Start")
        self.restartButton = Button(450, 300, 100, 50, "Again")
        self.chatBox = None
        self.turn = 1
        self.time = 0
        self.state = "START"
        self.myselfIndex = 0
        self.finished_player = 0
        self.play_state = {
            "hau": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "nguyen": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "nam": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "thien": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "is_finished": False,
        }

        self.web_socket_thread = WebSocketListenerThread(URI, self.response_come)
        self.web_socket_thread.daemon = True
        self.web_socket_thread.start()

    def __del__(self):
        self.web_socket_thread.stop()
        self.web_socket_thread.join()

    def send_command(self):
        print("push_game_state|" + json.dumps(self.play_state))
        self.web_socket_thread.set_command("push_game_state|" + json.dumps(self.play_state))

    def response_come(self, response):
        if self.state == "PLAY":
            if self.userName != "" and self.userName != "hau":
                self.play_state = json.loads(response)["play"]
                state = self.play_state
                print(state)
                for player in self.players:
                    if player.name in state:
                        state[player.name]["card_list"] = json.loads(state[player.name]["card_list"])
                        for c in state[player.name]["card_list"]:
                            found = False
                            for item in player.cards:
                                if item.to_string() == c:
                                    found = True
                            if not found:
                                n, s = c.split("-")
                                card = Card(n, s, SPRITE_SCALING_CARD)
                                if player.name == self.userName:
                                    card.up()
                                else:
                                    card.down()
                                card.center_x = 400
                                card.center_y = 300
                                player.add_card(card)
                if self.play_state["is_finished"]:
                    self.state = "FINISH"

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

        self.chatBox = ChatBox(50, 50, 150, 200, self.userName)

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

        self.play_state = {
            "hau": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "nguyen": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "nam": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "thien": {
                "card_list": [],
                "is_opened": False,
                "balance": 1000,
            },
            "is_finished": False,
        }

        if self.userName == "hau":
            self.send_command()

    def draw(self):
        if self.state == "START":
            self.startButton.draw()
        elif self.state == "LOGIN":
            self.userNameInput.draw()
            self.loginButton.draw()
        elif self.state == "BET":
            self.bidInput.draw()
            self.betButton.draw()
        elif self.state == "PLAY":
            for player in self.players:
                player.draw()
            self.cardsBox.draw()
            self.chatBox.draw()
        elif self.state == "FINISH":
            for player in self.players:
                for card in player.cards:
                    card.up()
                player.draw()
            self.restartButton.draw()
            self.chatBox.draw()

    def update(self):
        for index, player in enumerate(self.players):
            player.update()
        if self.userName == "hau":
            if self.state == "PLAY":
                self.time += 1
                if self.time == 300:
                    self.time = 0
                    self.players[self.turn % len(self.players)].is_distributed = True
                    self.turn += 1
                self.players[self.turn % len(self.players)].time = self.time / 60
        elif self.state == "PLAY":
            for player in self.players:
                if player.name in self.play_state:
                    if not player.is_distributed and self.play_state[player.name]["is_opened"]:
                        self.finished_player += 1
                        player.is_distributed = True
                        for card in player.cards:
                            card.up()

    def on_mouse_press(self, x, y):
        if self.state == "PLAY":
            if self.userName == "hau":
                if self.cardsBox.collides_with_point((x, y)) and not self.players[self.turn % len(self.players)].is_distributed:
                    card = self.cardsBox.get_card()
                    if self.players[self.turn % len(self.players)].name == self.userName:
                        card.up()
                    else:
                        card.down()
                    self.players[self.turn % len(self.players)].add_card(card)
                    self.play_state[self.players[self.turn % len(self.players)].name]["card_list"] = json.dumps([c.to_string() for c in self.players[self.turn % len(self.players)].cards])
                    self.send_command()
                    self.cardsBox.on_click()
                for player in self.players:
                    if player.collides_with_point((x, y)) and \
                            player.role != "me" and \
                            player.is_distributed:
                        for card in player.cards:
                            card.up()
                        self.play_state[player.name]["is_opened"] = True
                        self.calculate_cards_point(player)
                        self.finished_player += 1
                        if self.finished_player == 3:
                            self.state = "FINISH"
                            self.play_state["is_finished"] = True
                        self.send_command()
            self.chatBox.on_mouse_press(x, y)
        elif self.state == "BET":
            self.bidInput.on_mouse_press(x, y)
        elif self.state == "LOGIN":
            self.userNameInput.on_mouse_press(x, y)

    def on_mouse_release(self, x, y):
        if self.state == "PLAY":
            self.cardsBox.reset()
        elif self.state == "START":
            self.startButton.on_mouse_release(x, y)
            if self.startButton.is_pressed:
                self.startButton.is_pressed = False
                self.startButton.is_hovered = False
                self.state = "LOGIN"
        elif self.state == "LOGIN":
            self.loginButton.on_mouse_release(x, y)
            if self.loginButton.is_pressed:
                self.userName = self.userNameInput.text
                self.userNameInput.text = ""
                self.chatBox.name = self.userName
                self.loginButton.is_pressed = False
                self.loginButton.is_hovered = False
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
                if self.userName == "hau":
                    self.distribute_card_for_all()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.state == "START":
            self.startButton.on_mouse_motion(x, y, dx, dy)
        elif self.state == "FINISH":
            self.restartButton.on_mouse_motion(x, y, dx, dy)
        elif self.state == "BET":
            self.betButton.on_mouse_motion(x, y, dx, dy)
        elif self.state == "LOGIN":
            self.loginButton.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == "BET":
            self.bidInput.on_key_press(symbol, modifiers)
            if self.bidInput.is_entered:
                self.players[self.myselfIndex].bet(self.bidInput.text)
                self.state = "PLAY"
                self.bidInput.is_entered = False
                self.distribute_card_for_all()
        if self.state == "PLAY":
            self.chatBox.on_key_press(symbol, modifiers)
        if self.state == "LOGIN":
            self.userNameInput.on_key_press(symbol, modifiers)
            if self.userNameInput.is_entered:
                self.userName = self.userNameInput.text
                self.userNameInput.text = ""
                self.chatBox.name = self.userName
                self.state = "BET"
                self.userNameInput.is_entered = False

    def add_player(self, player):
        self.players.append(player)

    def distribute_card_for_all(self):
        for i in range(2):
            for p in self.players:
                card = self.cardsBox.get_card()
                if p.name == self.userName:
                    card.up()
                else:
                    card.down()
                p.add_card(card)
                self.play_state[p.name]["card_list"] = json.dumps(
                    [c.to_string() for c in p.cards])
        self.send_command()

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
        self.play_state[player.name]["point"] = player.balance
