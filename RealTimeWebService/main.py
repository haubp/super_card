import asyncio
import websockets


async def handle_client(websocket, path):
    # This function will be called whenever a new WebSocket client connects.
    try:
        while True:
            message = await websocket.recv()  # Wait for a message from the client
            print(f"Received: {message}")
            await websocket.send(f"You said: {message}")  # Send a response back
    except websockets.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
