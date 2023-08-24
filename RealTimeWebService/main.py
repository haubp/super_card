import asyncio
import websockets

CHAT_HISTORY = "hello world"


async def handle_client(websocket, path):
    global CHAT_HISTORY
    # This function will be called whenever a new WebSocket client connects.
    try:
        while True:
            message = await websocket.recv()  # Wait for a message from the client
            if message == "chat_history":
                await websocket.send(CHAT_HISTORY)  # Send a response back
            else:
                CHAT_HISTORY += ("\n" + message)
    except websockets.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
