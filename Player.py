import arcade
import threading
import websockets
import time
import asyncio


# --- Constants ---
URI = "ws://localhost:8765"


class WebSocketListenerThread(threading.Thread):
    def __init__(self, uri):
        super().__init__()
        self.uri = uri
        self.stop_event = threading.Event()
        self.realtime_data = None
        self.loop = None

    async def listen_to_websocket(self):
        async with websockets.connect(self.uri) as websocket:
            while not self.stop_event.is_set():
                try:
                    print("Ready to send data")
                    await websocket.send("Hello, WebSocket Server!")
                    response = await websocket.recv()
                    print(f"Received from server: {response}")
                    self.realtime_data = response
                    time.sleep(1)
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed.")
                    break

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.listen_to_websocket())

    def stop(self):
        if self.loop is not None:
            self.loop.call_soon_threadsafe(self.loop.stop)


class Player(arcade.Sprite):
    def __init__(self, is_host, role, name, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.cards = arcade.SpriteList()
        self.name = name
        self.is_host = is_host
        self.role = role
        self.is_distributed = False
        self.time = 0
        self.point = 100
        self.bid = 10
        self.balance = 1000
        self.ready = False

        self.web_socket_thread = WebSocketListenerThread(URI)
        self.web_socket_thread.start()

    def __del__(self):
        self.web_socket_thread.stop()
        self.web_socket_thread.join()

    def bet(self, b):
        self.bid = b

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for card in self.cards:
            card.draw()
        arcade.draw_text(self.name, self.center_x + 50, self.center_y + 15, arcade.color.WHITE, 14)
        arcade.draw_text("Bet: " + str(self.bid) + "$", self.center_x + 50, self.center_y - 5, arcade.color.WHITE, 14)
        arcade.draw_text("Balance: " + str(self.balance) + "$", self.center_x + 50, self.center_y - 30, arcade.color.WHITE, 14)
        if not self.is_distributed and self.time > 0:
            arcade.draw_arc_outline(self.center_x, self.center_y, 55, 55, arcade.color.YELLOW_ROSE
                                    , 0, self.time * 72, 10)
        super().draw()

    def update(self):
        for index, card in enumerate(self.cards):
            if self.center_y > 300:
                if card.center_y < self.center_y - 70:
                    card.center_y += 10
                elif card.center_y > self.center_y - 70:
                    card.center_y -= 10
            else:
                if card.center_y < self.center_y + 70:
                    card.center_y += 10
                elif card.center_y > self.center_y + 70:
                    card.center_y -= 10

            if card.center_x < self.center_x + index * 10:
                card.center_x += 10
            elif card.center_x > self.center_x + index * 10:
                card.center_x -= 10

    def add_card(self, card):
        if card is not None:
            self.cards.append(card)

    def get_cards_point(self):
        total_point = 0
        for c in self.cards:
            if c.num < 10:
                total_point += c.num
            else:
                total_point += 10
        return total_point
