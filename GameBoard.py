import arcade


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.1
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


class GameBoard(arcade.Window):

    def __init__(self, game):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Card Game")

        self.game = game

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.game.setup()

    def on_draw(self):
        arcade.start_render()
        self.game.draw()

    def update(self, delta_time: float):
        self.game.update()

    def on_mouse_press(self, x, y, button, modifiers):
        self.game.on_mouse_press(x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.game.on_mouse_release(x, y)

    def on_key_press(self, symbol: int, modifiers: int):
        self.game.on_key_press(symbol, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.game.on_mouse_motion(x, y, dx, dy)