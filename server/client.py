import asyncio
import websockets

async def hello():
    uri = "ws://192.168.1.9:5001"  # Adres serwera WebSocket        DO ZMIANY !!!

    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Wpisz wiadomość do wysłania (lub 'quit' aby wyjść): ")
            if message.lower() == 'quit':
                break

            await websocket.send(message)
            response = await websocket.recv()
            print(f"Odpowiedź od serwera: {response}")

asyncio.run(hello())