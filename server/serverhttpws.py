import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style

SERVER = "192.168.1.9"
PORT_HTTP = 5000
PORT_WS = 5001

connected = set() # copy of all websocets curently connected
http_server = None
ws_server = None
# ==============================================================

class ServerHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>Hello</h1></body></html>", "utf-8"))

async def ws_handler(websocket, path):
    connected.add(websocket)
    print(f"{Fore.LIGHTYELLOW_EX}[WEBSOCKET SERVER] Client connected !! {Style.RESET_ALL}")         # client connected

    try:
        async for message in websocket:                                                             # odczytywanie wiadomości asynchronicznie. Ciągle oczekuje na nowe wiadomości od klienta
            print(f"{Fore.LIGHTMAGENTA_EX}[SERVER WEBSOCKET] Recieved message from client: {message} {Style.RESET_ALL}")    # recieved message
            response = f"Received: {message}"
            await websocket.send(response)
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET] {response} {Style.RESET_ALL}")      # response to client
    except websockets.exceptions.ConnectionClosed as ex:
        pass
    finally:
        connected.remove(websocket)
        print(f"{Fore.LIGHTRED_EX}[WEBSOCKET SERVER] Client disconnected !! {Style.RESET_ALL}\n")            # client disconnected

async def main():
    global http_server, ws_server

    http_server = HTTPServer((SERVER, PORT_HTTP), ServerHttp)
    http_server_thread = asyncio.get_event_loop().run_in_executor(None, http_server.serve_forever)
    print(f"{Fore.GREEN}[STARTED HTTP SERVER] server is running on:{Style.RESET_ALL} {Fore.CYAN}{SERVER}:{PORT_HTTP}{Style.RESET_ALL}")

    ws_server = await websockets.serve(
        ws_handler,
        SERVER,
        PORT_WS,
        ping_interval=None, # nierozłączanie klienta z serwerem
        ping_timeout=None
    )
    print(f"{Fore.LIGHTGREEN_EX}[STARTED WEBSOCKET SERVER] server is running on:{Style.RESET_ALL} {Fore.CYAN}{SERVER}:{PORT_WS}{Style.RESET_ALL}\n")

    try:
        await asyncio.gather(http_server_thread, ws_server.wait_closed()) # jednoczesne oczekiwanie na zakończenie dwóch zadań
    except KeyboardInterrupt:
        pass
    finally:
        if http_server:
            http_server.shutdown()
            print(f"{Fore.LIGHTRED_EX}[STOPPED HTTP SERVER{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}SUCCESSFULLY]{Style.RESET_ALL}")
        if ws_server:
            ws_server.close()
            await ws_server.wait_closed()
            print(f"{Fore.LIGHTRED_EX}[STOPPED WEBSOCKET SERVER{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}SUCCESSFULLY]{Style.RESET_ALL}")

asyncio.run(main())