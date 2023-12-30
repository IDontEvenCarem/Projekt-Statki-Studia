import asyncio
import websockets
import json
from colorama import Fore, Style

async def hello():
    uri = "ws://85.89.170.62:5001"  # Adres serwera WebSocket        DO ZMIANY !!!

    async with websockets.connect(uri) as websocket:

        # Odebranie i wyświetlenie mojego unikalnego id na serwerze
        response = await websocket.recv()
        data = json.loads(response)
        my_id = data.get('my_id')
        print(f"{Fore.LIGHTYELLOW_EX}[WEBSOCKET CLIENT] client({my_id}) connected !! {Style.RESET_ALL}")

        # Podaje unikalne id gracza z którym chce grać
        enemy_player_id = input("Wpisz id gracza z którym chcesz grać: ")


        # Jestem graczem rozpoczynającym grę więc pierwszy wysyłam koordynaty
        after_firs_move = False
        if not after_firs_move:

            # Wykonuję swój pierwszy ruch
            coordinates = input("Wpisz koordynaty do wysłania (lub 'quit' aby wyjść): ")
            if coordinates.lower() == 'quit':
                exit()

            # Wysyłam pierwsze koordynaty w grz (wykonuję pierwszy ruch)
            response_data = {"coordinates": f"{coordinates}", "my_id": f"{my_id}", "enemy_player_id": f"{enemy_player_id}"}
            response_json = json.dumps(response_data)
            await websocket.send(response_json)

            # Otrzymuje odpowiedź od serwera czy wysłałem poprawną wiadomość
            response = await websocket.recv()
            data = json.loads(response)
            response_status = data.get('response_status')
            if "200" == response_status:
                print(f"{Fore.GREEN}[WEBSOCKET CLIENT] Czy Twoja wiadomosc byla poprawna?: {str(response_status)} {Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[WEBSOCKET CLIENT] Czy Twoja wiadomosc byla poprawna?: {str(response_status)} {Style.RESET_ALL}")
            
            # To kończy pierwszy ruch
            after_firs_move = True

        # Każdy kolejny ruch w grze
        while after_firs_move:
            
            # Oczekuję na informację o ruchu oponenta
            response = await websocket.recv()
            data = json.loads(response)
            coordinates = data.get('coordinates')
            print(f"{Fore.BLUE}[WEBSOCKET CLIENT] Przeciwnik strzelil w pole: {str(coordinates)} {Style.RESET_ALL}")

            # Wykonuję swój kolejny ruch
            coordinates = input("Wpisz wiadomość do wysłania (lub 'quit' aby wyjść): ")
            if coordinates.lower() == 'quit':
                break
            
            # Wysyłam kolejne koordynaty
            response_data = {"coordinates": f"{coordinates}", "my_id": f"{my_id}", "enemy_player_id": f"{enemy_player_id}"}
            response_json = json.dumps(response_data)
            await websocket.send(response_json)
            
            # Otrzymuje odpowiedź od serwera czy wysłałem poprawną wiadomość
            response = await websocket.recv()
            data = json.loads(response)
            response_status = data.get('response_status')
            if "200" == response_status:
                print(f"{Fore.GREEN}[WEBSOCKET CLIENT] Czy Twoja wiadomosc byla poprawna?: {str(response_status)} {Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[WEBSOCKET CLIENT] Czy Twoja wiadomosc byla poprawna?: {str(response_status)} {Style.RESET_ALL}")
                
        
            


asyncio.run(hello())