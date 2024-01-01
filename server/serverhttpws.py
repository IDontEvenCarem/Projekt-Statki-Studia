import asyncio
import websockets
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style

SERVER = "0.0.0.0"
PORT_HTTP = 5000
PORT_WS = 5001

connected = set() # copy of all websocets curently connected
http_server = None
ws_server = None
clients = {}
# ==============================================================

# Do sprawdzania czy dobrze działa sprawdzanie statusu wiadomości i odsyłanie ich
def czy_poprawne_wspolrzedne(wspolrzedne):

    # Sprawdź, czy współrzędne mają poprawny format
    if len(wspolrzedne) < 2:
        print("Dlugosc wspolrzednej: " + str(len(wspolrzedne)))
        return False

    litera, cyfra = wspolrzedne[0].upper(), wspolrzedne[1]
 
    # Sprawdź, czy litera jest w zakresie kolumn
    if litera < 'A' or litera > 'J':
        print(" Czy litera zawarta w przedziale (Nie): " + litera)
        return False

    # Sprawdź, czy cyfra mieści się w zakresie wierszy
    try:
        cyfra = int(cyfra)
        if not (1 <= cyfra <= 10):
            print(" Czy cyfra zawarta w przedziale (Nie): " + str(cyfra))
            return False
    except ValueError:
        return False
    # print("Przeanalizowane dane: " + litera + str(cyfra))
    return True


class ServerHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>Hello</h1></body></html>", "utf-8"))

async def ws_handler(websocket, path):
    connected.add(websocket)

    # Generuj unikalny identyfikator klienta
    client_id = id(websocket)
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
            coordinates = data.get('coordinates')
            enemy_player_id = int(data.get('enemy_player_id'))

            # Wyświetlenie zawartości pliku JSON
            print(f"{Fore.LIGHTMAGENTA_EX}[SERVER WEBSOCKET] Recieved message from client({client_id}): {data} {Style.RESET_ALL}")    # recieved message

            # Sprawdzenie czy wysłane współrzędne są poprawnego formatu i zakresu
            if czy_poprawne_wspolrzedne(coordinates):
                response_status = "200"
            else:
                response_status = "400"
            
            # Przesłanie klientowi informacji czy wysłał dobre współrzędne
            response_data = {"type": "RESPONSE", "response_status": f"{response_status}"}
            response_json = json.dumps(response_data)
            await websocket.send(response_json)

            # Wyświetlenie dodatkowych informacji na serwerze
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - RS] {response_status} {Style.RESET_ALL}")     
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - CCID] {client_id} {Style.RESET_ALL}")      
            print(f"{Fore.MAGENTA}[SERVER WEBSOCKET - CEPID] {enemy_player_id} {Style.RESET_ALL}")     

            # Przekaż wiadomość od gracza do jego przeciwnika
            # await send_to_other_client(clients[client_id], coordinates, clients[enemy_player_id], enemy_player_id)
            await send_to_client(enemy_player_id, coordinates, client_id)

    except websockets.exceptions.ConnectionClosed as ex:
        pass
    finally:
        connected.remove(websocket)
        print(f"{Fore.LIGHTRED_EX}[WEBSOCKET SERVER] client({client_id}) disconnected !! {Style.RESET_ALL}\n")            # client disconnected

# Prześlij wiadomośc do konkretnego klienta
async def send_to_client(enemy_player_id, coordinates, sender):
    # Sprawdź, czy klient istnieje w liście
    if enemy_player_id in clients:
        # Pobierz obiekt WebSocket dla danego klienta
        client_socket = clients[enemy_player_id]

        # Serializuj dane do formatu JSON
        response_data = {"type": "ENEMY_SHOT", "coordinates": f"{coordinates}", "my_id": sender, "enemy_player_id": f"{enemy_player_id}"}
        response_json = json.dumps(response_data)

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