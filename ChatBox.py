import arcade
from TextInput import *
from Button import *


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

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        self.chatInput.draw()

        arcade.draw_rectangle_filled(self.center_x + 40, self.center_y + 120, self.width, self.height,
                                     arcade.color.AMAZON)
        arcade.draw_rectangle_outline(self.center_x + 40, self.center_y + 120, self.width, self.height,
                                      arcade.color.BLACK_OLIVE)
        for index, text in enumerate(self.chatHistory):
            arcade.draw_text(text, self.center_x - 20, self.center_y + 200 - index * 15,
                             arcade.color.WHITE, 10)

    def on_mouse_press(self, x, y):
        self.chatInput.on_mouse_press(x, y)

    def on_key_press(self, symbol, modifiers):
        self.chatInput.on_key_press(symbol, modifiers)
        if symbol == arcade.key.ENTER:
            self.chatHistory.append(self.name + ": " + self.chatInput.text)
            self.chatInput.text = ""

