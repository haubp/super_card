import asyncio
import websockets
import json
from DB import *

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
            elif command == "save":
                balance_info = json.loads(content)
                print("Hau balance: ", balance_info["hau"]["balance"])
                print("Nguyen balance: ", balance_info["nguyen"]["balance"])
                print("Nam balance: ", balance_info["nam"]["balance"])
                print("Thien balance: ", balance_info["thien"]["balance"])
                balances = {1: balance_info["hau"]["balance"],
                            2: balance_info["nguyen"]["balance"],
                            3: balance_info["nam"]["balance"],
                            4: balance_info["thien"]["balance"]}

                update_users_balance(balances)
                await websocket.send("OK")

    except websockets.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
