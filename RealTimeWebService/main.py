import asyncio
import websockets
import json

CHAT_HISTORY = ""
GAME_STATE = {
    "play": {},
    "chat_history": CHAT_HISTORY
}


async def handle_client(websocket, path):
    global CHAT_HISTORY
    global GAME_STATE
    # This function will be called whenever a new WebSocket client connects.
    try:
        while True:
            message = await websocket.recv()  # Wait for a message from the client
            command, content = message.split('|')

            if command == "receive_game_state":
                await websocket.send(json.dumps(GAME_STATE))
            elif command == "push_game_state":
                GAME_STATE["play"] = json.loads(content)
                await websocket.send("OK")
            elif command == "chat":
                CHAT_HISTORY += ("\n" + content)
                GAME_STATE["chat_history"] = CHAT_HISTORY
                await websocket.send("OK")
    except websockets.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
