import asyncio
import websockets
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style
import game_logic
import random
import string
from typing import Dict, Any

SERVER = "0.0.0.0"
PORT_HTTP = 5000
PORT_WS = 5001

connected = dict() # copy of all websocets curently connected (websocket.remote_address -> websocket)
http_server = None
ws_server = None
clients = {}

def inform_client(client_id, data):
    print(f"{Fore.LIGHTMAGENTA_EX}[SERVER WEBSOCKET] Informing client({client_id}): {data} {Style.RESET_ALL}")
    if client_id in clients:
        client_socket = clients[client_id]
        response_json = json.dumps(data)
        asyncio.run_coroutine_threadsafe(client_socket.send(response_json), asyncio.get_event_loop())

# ==============================================================

class GameManager:
    def __init__(self, send_to_client_hook):
        # mapa player_id -> game_id
        self.player_game_map : Dict[str, Any] = {}
        # mapa game_id -> player_id[]
        self.game_player_map : Dict[str, Any] = {}
        # mapa game_id -> Game
        self.game_map : Dict[str, game_logic.WarshipsGame] = {}
        self.send_to_client_hook = send_to_client_hook

    def create_game(self, player_id):
        game_id = self.generate_game_id()
        game = game_logic.WarshipsGame()
        self.game_map[game_id] = game
        self.player_game_map[player_id] = game_id
        self.game_player_map[game_id] = [player_id]
        return game_id

    def join_game(self, player_id, game_id):
        game = self.game_map[game_id]
        game.add_player(player_id)
        self.player_game_map[player_id] = game_id
        other_player_id = self.game_player_map[game_id][0]
        self.game_player_map[game_id].append(player_id)
        return other_player_id

    def generate_game_id(self):
        while True:
            game_id = "".join(random.sample(string.ascii_letters + string.digits, 6))
            if game_id not in self.game_map:
                return game_id
    
game_manager = GameManager(send_to_client_hook=inform_client)

# ==============================================================

class ServerHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>Hello</h1></body></html>", "utf-8"))

async def ws_handler(websocket, path):
    connected[websocket.remote_address] = websocket

    # Generuj unikalny identyfikator klienta
    client_id = websocket.remote_address
    # Przypisz klienta do słownika
    clients[client_id] = websocket

    # Client connected
    print(f"{Fore.LIGHTYELLOW_EX}[WEBSOCKET SERVER] client({client_id}) connected !! {Style.RESET_ALL}")  

    # Wysłanie klientowi jego unikalnego id
    response_data = {"type": "INITIAL_ID", "my_id": f"{client_id}"}
    response_json = json.dumps(response_data)
    await clients[client_id].send(response_json)

    # Odczytywanie wiadomości asynchronicznie. Ciągle oczekuje na nowe wiadomości od klienta
    try:
        async for message in websocket:           
            # Odczytywanie informacji z pliku JSON
            data = json.loads(message)

            print(f"{Fore.LIGHTMAGENTA_EX}[SERVER WEBSOCKET] Recieved message from client({client_id}): {data} {Style.RESET_ALL}")    # recieved message

            type = data.get('type')
            request_id = data.get('request_id')

            response_data = {}
            response_status = "ERROR"

            if type == "create_game":
                game_id = game_manager.create_game(player_id=client_id)
                response_data['game_id'] = game_id
                response_status = "OK"
            elif type == "join_game":
                other_player_id = game_manager.join_game(player_id=client_id, game_id=data['game_id'])
                response_status = "OK"
                await send_to_client(other_player_id, {"type": "enemy_joined", "enemy_player_id": client_id})
            else:
                response_status = "ERROR"
                response_data['error'] = f"Unknown action: {type}"
                print(f"{Fore.LIGHTRED_EX}[SERVER WEBSOCKET] Unknown action: {type} {Style.RESET_ALL}")

            response_data['type'] = "response"
            response_data['request_id'] = request_id
            response_data['status'] = response_status
            response_json = json.dumps(response_data)
            await websocket.send(response_json)

            # Wyświetlenie dodatkowych informacji na serwerze
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - RS] {response_status} {Style.RESET_ALL}")     
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - CCID] {client_id} {Style.RESET_ALL}")      
            # print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - CEPID] {enemy_player_id} {Style.RESET_ALL}")     

            # Przekaż wiadomość od gracza do jego przeciwnika
            # await send_to_other_client(clients[client_id], coordinates, clients[enemy_player_id], enemy_player_id)
            # await send_to_client(enemy_player_id, coordinates, client_id)

    except websockets.exceptions.ConnectionClosed as ex:
        pass
    finally:
        del connected[websocket.remote_address]
        print(f"{Fore.LIGHTRED_EX}[WEBSOCKET SERVER] client({client_id}) disconnected !! {Style.RESET_ALL}\n")            # client disconnected

# Prześlij wiadomośc do konkretnego klienta
async def send_to_client(player_id, data: dict):
    # Sprawdź, czy klient istnieje w liście
    if player_id in clients:
        # Pobierz obiekt WebSocket dla danego klienta
        client_socket = clients[player_id]

        # Serializuj dane do formatu JSON
        response_json = json.dumps(data)

        # Wyślij odpowiedź do klienta
        await client_socket.send(response_json)

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
            # await send_to_all("STOPPING HTTP SERVER!")
            http_server.shutdown()
            print(f"{Fore.LIGHTRED_EX}[STOPPED HTTP SERVER{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}SUCCESSFULLY]{Style.RESET_ALL}")
        if ws_server:
            print("Aktywne połączenia:")
            for connection in connected:
                print(f"- {connection.remote_address}")
            ws_server.close()
            await ws_server.wait_closed()
            print(f"{Fore.LIGHTRED_EX}[STOPPED WEBSOCKET SERVER{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}SUCCESSFULLY]{Style.RESET_ALL}")

asyncio.run(main())