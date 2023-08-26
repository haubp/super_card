import threading
import websockets
import time
import asyncio

# --- Constants ---
URI = "ws://localhost:8765"


class WebSocketListenerThread(threading.Thread):
    def __init__(self, uri, response_callback):
        super().__init__()
        self.uri = uri
        self.stop_event = threading.Event()
        self.loop = None
        self.response_callback = response_callback
        self.command = ""

    def set_command(self, command):
        self.command = command

    async def listen_to_websocket(self):
        async with websockets.connect(self.uri) as websocket:
            while not self.stop_event.is_set():
                try:
                    if self.command != "":
                        await websocket.send(self.command)
                        await websocket.recv()
                        self.command = ""
                    else:
                        await websocket.send("receive_chat_history|")
                        response = await websocket.recv()
                        self.response_callback(response)
                    time.sleep(0.5)
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
