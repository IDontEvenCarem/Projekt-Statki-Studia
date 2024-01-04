import collections

ship_shapes = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}

FieldStatus = collections.namedtuple("FieldStatus", ["hasShip", "isHit"])
Position = collections.namedtuple("Position", ["x", "y"])
ShipPosition = collections.namedtuple("ShipPosition", ["coords", "direction"])

class WarshipsGame:
    def __init__(self):
        self.boardLeft = [[FieldStatus(hasShip=False, isHit=False) for _ in range(10)] for _ in range(10)]
        self.boardRight = [[FieldStatus(hasShip=False, isHit=False) for _ in range(10)] for _ in range(10)]
        self.shipsLeft = {ship: None for ship in ship_shapes}
        self.shipsRight = {ship: None for ship in ship_shapes}
        self.leftReady = False
        self.rightReady = False

        self.gameStarted = False
        self.gameEnded = False
        self.currentPlayer = None
        self.winner = None

    # ================================
    # ====== Game state methods ======
    # ================================

    def is_player_ready(self, player):
        ships = self.shipsLeft if player == "left" else self.shipsRight
        readyness = self.leftReady if player == "left" else self.rightReady
        print(ships)
        all_ships_placed = all([pos is not None for ship, pos in ships.items()])
        return all_ships_placed and readyness

    def remaining_ships(self, player):
        ships = self.shipsLeft if player == "left" else self.shipsRight
        return {ship for ship in ships if ships[ship][1] is None}

    def can_start_game(self):
        return self.is_player_ready("left") and self.is_player_ready("right")

    def get_board_string(self, player):
        if player == "left":
            board = self.boardLeft
        else:
            board = self.boardRight

        board_string = "["
        for y in range(10):
            for x in range(10):
                if board[x][y].hasShip and board[x][y].isHit:
                    board_string += "X"
                elif board[x][y].hasShip:
                    board_string += "#"
                elif board[x][y].isHit:
                    board_string += "~"
                else:
                    board_string += " "
        board_string += "]"

        return board_string
    
    def is_ship_sunk(self, player, ship):
        if player == "left":
            board = self.boardLeft
            ships = self.shipsLeft
        else:
            board = self.boardRight
            ships = self.shipsRight

        if ship not in ships:
            raise Exception("Invalid ship type")

        position = self.coords_to_position(ships[ship][0])

        if ships[ship][1] == "horizontal":
            for i in range(ship_shapes[ship]):
                if not board[position.x + i][position.y].isHit:
                    return False
        else:
            for i in range(ship_shapes[ship]):
                if not board[position.x][position.y + i].isHit:
                    return False

        return True
    
    def all_ships_sunk(self, player):
        ships = self.shipsLeft if player == "left" else self.shipsRight
        return all([self.is_ship_sunk(player, ship) for ship in ships])

    # ==========================
    # ====== Game actions ======
    # ==========================

    def place_ship(self, player, ship, coordinates, direction):
        if self.gameStarted:
            raise Exception("Game already started")

        if player == "left":
            board = self.boardLeft
            ships = self.shipsLeft
        else:
            board = self.boardRight
            ships = self.shipsRight

        if ship not in ships:
            raise Exception("Invalid ship type")

        if not self.are_coords_valid(coordinates):
            raise Exception("Invalid coordinates")

        position = self.coords_to_position(coordinates)

        if direction == "horizontal":
            if position.x + ship_shapes[ship] > 10:
                raise Exception("Ship out of bounds")
            for i in range(ship_shapes[ship]):
                if board[position.x + i][position.y].hasShip:
                    raise Exception("Ship already placed here")
        else:
            if position.y + ship_shapes[ship] > 10:
                raise Exception("Ship out of bounds")
            for i in range(ship_shapes[ship]):
                if board[position.x][position.y + i].hasShip:
                    raise Exception("Ship already placed here")

        if direction == "horizontal":
            for i in range(ship_shapes[ship]):
                board[position.x + i][position.y] = FieldStatus(hasShip=True, isHit=False)
        else:
            for i in range(ship_shapes[ship]):
                board[position.x][position.y + i] = FieldStatus(hasShip=True, isHit=False)

        ships[ship] = (coordinates, direction)
        return True

    def remove_ship(self, player, ship):
        if self.gameStarted:
            raise Exception("Game already started")

        if player == "left":
            board = self.boardLeft
            ships = self.shipsLeft
        else:
            board = self.boardRight
            ships = self.shipsRight

        if ship not in ships:
            return False

        position = self.coords_to_position(ships[ship][0])

        if ships[ship][1] == "horizontal":
            for i in range(ship_shapes[ship]):
                board[position.x + i][position.y] = FieldStatus(hasShip=False, isHit=False)
        else:
            for i in range(ship_shapes[ship]):
                board[position.x][position.y + i] = FieldStatus(hasShip=False, isHit=False)

        ships[ship] = (None, None)
        return True

    def start_game(self):
        if self.gameStarted:
            raise Exception("Game already started")

        if not self.can_start_game():
            raise Exception("Cannot start game yet")

        self.gameStarted = True
        self.currentPlayer = "left"
        return True
    
    def take_shot(self, player, coordinates):
        if not self.gameStarted:
            raise Exception("Game not started yet")
        
        if self.gameEnded:
            raise Exception("Game already ended")
        
        if self.currentPlayer != player:
            raise Exception("Not your turn")

        if player == "left":
            board = self.boardRight
        else:
            board = self.boardLeft
        
        if not self.are_coords_valid(coordinates):
            return False
        
        position = self.coords_to_position(coordinates)
        
        field = board[position.x][position.y]

        if field.isHit:
            return False
        
        board[position.x][position.y] = FieldStatus(hasShip=field.hasShip, isHit=True)
        
        if field.hasShip:
            if player == "left":
                self.shipsRight = {ship: (coords, direction) if coords != coordinates else (coords, direction) for ship, (coords, direction) in self.shipsRight.items()}
                if self.all_ships_sunk("right"):
                    self.gameEnded = True
                    self.winner = "left"
            else:
                self.shipsLeft = {ship: (coords, direction) if coords != coordinates else (coords, direction) for ship, (coords, direction) in self.shipsLeft.items()}
                if self.all_ships_sunk("left"):
                    self.gameEnded = True
                    self.winner = "right"
        
        if not board[position.x][position.y].hasShip:
            self.currentPlayer = "left" if self.currentPlayer == "right" else "right"
        
        return True

    def mark_ready(self, player):
        if self.gameStarted:
            raise Exception("Game already started")

        if player == "left":
            self.leftReady = True
        else:
            self.rightReady = True

        return True

    # ===============================
    # ====== Utility functions ======
    # ===============================
    def coords_to_position(self, coords):
        return Position(ord(coords[0]) - ord('A'), int(coords[1:]) - 1)
    
    def position_to_coords(self, position):
        return chr(position.x + ord('A')) + str(position.y + 1)
    
    def are_coords_valid(self, coords):
        if len(coords) < 2:
            return False
        letter, number = coords[0].upper(), coords[1]
        if letter < 'A' or letter > 'J':
            return False
        try:
            number = int(number)
            if not (1 <= number <= 10):
                return False
        except ValueError:
            return False
        return True
    
    def print_board(self, player):
        if player == "left":
            board = self.boardLeft
        else:
            board = self.boardRight
        
        print("  1 2 3 4 5 6 7 8 9 10")
        for y in range(10):
            print(chr(ord('A') + y), end=" ")
            for x in range(10):
                if board[x][y].hasShip and board[x][y].isHit:
                    print("X", end=" ")
                elif board[x][y].hasShip:
                    print("#", end=" ")
                elif board[x][y].isHit:
                    print("~", end=" ")
                else:
                    print(" ", end=" ")
            print()


# ===================
# ====== Tests ======
# ===================
if __name__ == "__main__":
    game = WarshipsGame()
    game.place_ship("left", "carrier", "A1", "vertical")
    game.place_ship("left", "battleship", "B1", "vertical")
    game.place_ship("left", "cruiser", "C1", "vertical")
    game.place_ship("left", "submarine", "D1", "vertical")
    game.place_ship("left", "destroyer", "E1", "vertical")
    game.place_ship("right", "carrier", "A1", "vertical")
    game.place_ship("right", "battleship", "B1", "vertical")
    game.place_ship("right", "cruiser", "C1", "vertical")
    game.place_ship("right", "submarine", "D1", "vertical")
    game.place_ship("right", "destroyer", "E1", "vertical")
    game.mark_ready("left")
    game.mark_ready("right")
    game.start_game()
    game.print_board("left")
    game.print_board("right")
    game.take_shot("left", "A1")
    game.take_shot("left", "B1")
    game.take_shot("left", "C1")
    game.take_shot("left", "D1")
    game.take_shot("left", "E1")
    game.take_shot("left", "F1")
    game.print_board("left")
    game.print_board("right")
    print(game.get_board_string("left"))
    print(game.get_board_string("right"))
    print(game.winner)