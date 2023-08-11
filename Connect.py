import asyncio
import websockets


async def connect_and_send():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket Server!")
        response = await websocket.recv()
        print(f"Received from server: {response}")

asyncio.get_event_loop().run_until_complete(connect_and_send())
