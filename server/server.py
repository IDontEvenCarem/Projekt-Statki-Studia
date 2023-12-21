import websockets
import asyncio
from colorama import Fore, Style

PORT = 5000

print(f"{Fore.LIGHTGREEN_EX}[STARTING] server is starting . . .{Style.RESET_ALL}")
print(f"{Fore.LIGHTGREEN_EX}[STARTED] server is running on port:{Style.RESET_ALL} {Fore.CYAN}{PORT}{Style.RESET_ALL}\n")
# ===============================================

connected = set() # copy of all websocets curently connected

async def server(websocket, path):
    print(f"{Fore.LIGHTYELLOW_EX}[SERVER] Client connected{Style.RESET_ALL}\n")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"{Fore.LIGHTMAGENTA_EX}[SERVER] Recieved message from client: {message} {Style.RESET_ALL}\n")
            for conn in connected:
                if conn != websocket:
                    await conn.send((f"{Fore.LIGHTBLUE_EX} {message}{Style.RESET_ALL}\n"))
    except websockets.exceptions.ConnectionClosed as ex:
        print(f"{Fore.LIGHTRED_EX}[SERVER] Client disconnected {Style.RESET_ALL}\n")
    finally:
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()