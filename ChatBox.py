import arcade
from TextInput import *
from Button import *
from Utils.WebSocketListenerThread import  *
import json


class ChatBox(arcade.Sprite):
    def __init__(self, center_x, center_y, w, h, n):
        super().__init__()

        self.width = w
        self.height = h
        self.center_x = center_x
        self.center_y = center_y
        self.name = n

        self.chatInput = TextInput(self.center_x + 40, self.center_y, 150, 25)
        self.chatHistory = []
        self.currentChat = []

        self.web_socket_thread = WebSocketListenerThread(URI, self.response_come)
        self.web_socket_thread.daemon = True
        self.web_socket_thread.start()

    def __del__(self):
        self.web_socket_thread.stop()
        self.web_socket_thread.join()

    def response_come(self, response):
        chat = json.loads(response)["chat_history"]
        self.chatHistory = chat.splitlines()
        self.currentChat = self.chatHistory[-12:]

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        self.chatInput.draw()

        arcade.draw_rectangle_filled(self.center_x + 40, self.center_y + 120, self.width, self.height,
                                     arcade.color.AMAZON)
        arcade.draw_rectangle_outline(self.center_x + 40, self.center_y + 120, self.width, self.height,
                                      arcade.color.BLACK_OLIVE)
        for index, text in enumerate(self.currentChat):
            arcade.draw_text(text, self.center_x - 20, self.center_y + 200 - index * 15,
                             arcade.color.WHITE, 10)

    def on_mouse_press(self, x, y):
        self.chatInput.on_mouse_press(x, y)

    def on_key_press(self, symbol, modifiers):
        self.chatInput.on_key_press(symbol, modifiers)
        if self.chatInput.is_entered and symbol == arcade.key.ENTER:
            self.web_socket_thread.set_command("chat|" + self.name + ": " + self.chatInput.text)
            self.chatInput.text = ""
            self.chatInput.is_entered = False
