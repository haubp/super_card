import arcade

class Button(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height, text, font_size=20, color=arcade.color.WHITE, button_color=arcade.color.BLUE):
        super().__init__()

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.color = color
        self.button_color = button_color

        self.is_hovered = False
        self.is_pressed = False

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height,
                                     self.button_color if not self.is_hovered else arcade.color.GREEN)
        arcade.draw_text(self.text, self.center_x - self.width / 2 + 10, self.center_y - 10, self.color, self.font_size,
                         anchor_x='left', anchor_y='center')

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovered = (self.center_x - self.width / 2) <= x <= (self.center_x + self.width / 2) and \
                          (self.center_y - self.height / 2) <= y <= (self.center_y + self.height / 2)

    def on_mouse_release(self, x, y):
        if self.is_hovered:
            self.is_pressed = True