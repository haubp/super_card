import arcade

class TextInput(arcade.Sprite):
    def __init__(self, center_x, center_y, w, h):
        super().__init__()

        self.width = w
        self.height = h
        self.center_x = center_x
        self.center_y = center_y

        self.text = ""
        self.text_color = arcade.color.BLACK

        self.input_box_active = False

        self.is_entered = False

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()

        if self.input_box_active:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.color.WHITE)
            arcade.draw_text(self.text, self.center_x - self.width / 2 + 10, self.center_y - 10, self.text_color, 20)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.color.GRAY)
            arcade.draw_text(self.text, self.center_x - self.width / 2 + 10, self.center_y - 10, self.text_color, 20)

    def on_mouse_press(self, x, y):
        if (self.center_x - self.width / 2) <= x <= (self.center_x + self.width / 2) and \
           (self.center_y - self.height / 2) <= y <= (self.center_y + self.height / 2):
            self.input_box_active = True
        else:
            self.input_box_active = False

    def on_key_press(self, symbol, modifiers):
        if self.input_box_active:
            if symbol == arcade.key.BACKSPACE:
                self.text = self.text[:-1]
            elif symbol == arcade.key.ENTER:
                self.input_box_active = False
                self.is_entered = True
            elif symbol == arcade.key.ESCAPE:
                self.text = ""
            else:
                self.text += chr(symbol)
