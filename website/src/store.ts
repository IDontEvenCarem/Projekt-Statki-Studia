import { defineStore } from "pinia";
import { CommunicationApi } from "./comms";

type ShipName = "carrier" | "battleship" | "cruiser" | "submarine" | "destroyer";

type Number = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
function makeEmptyCellsStatus() : Record<`${Number};${Number}`, "empty" | "hit" | "miss">  {
    const obj : any = {};
    for (let x = 1; x <= 10; x++) {
        for (let y = 1; y <= 10; y++) {
            obj[`${x};${y}`] = "empty";
        }
    }
    return obj;    
}

export const useStore = defineStore('mainStore', {
    state: () => ({
        connection: undefined as undefined | CommunicationApi,
        game_id: undefined as string | undefined,
        phase: "main-menu" as "main-menu" | "placing-ships" | "waiting-for-other-player" | "playing" | "game-over",
        self_won: false,
        own_status: "present" as "present" | "ready" | "playing",
        other_player_status: "not-present" as "not-present" | "present" | "ready" | "playing",
        my_turn: false,
        ships: [
            { name: "carrier" as ShipName, size: 5, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "battleship" as ShipName, size: 4, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "cruiser" as ShipName, size: 3, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "submarine" as ShipName, size: 3, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "destroyer" as ShipName, size: 2, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
        ],
        currentShip: undefined as undefined | "carrier" | "battleship" | "cruiser" | "submarine" | "destroyer",
        requestRunning: false,
        ownCellStatus: makeEmptyCellsStatus(),
        enemyCellStatus: makeEmptyCellsStatus(),
        toasts: [] as { text: string, type: "info" | "error" }[],
    }),

    actions: {
        setConnection(connection: CommunicationApi) {
            this.connection = connection;
            this.connection.addEventListener('message', e => {
                const data = (e as CustomEvent).detail as any;
                if (data.type === 'enemy_joined') {
                    this.other_player_status = "present";
                }
                else if (data.type === 'game_start') {
                    this.phase = "playing";
                }
                else if (data.type === 'game_over') {
                    this.phase = "game-over";
                }
                else if (data.type === "waiting_for_opponent") {
                    this.phase = 'waiting-for-other-player'
                }
                else if (data.type === "shot") {
                    const { x, y, hit, is_game_won } = data;
                    const cell = `${x};${y}`;
                    if (cell in this.ownCellStatus) {
                        (this.ownCellStatus as any)[cell] = hit ? "hit" : "miss";
                    }
                    if (is_game_won) {
                        this.phase = "game-over";
                        this.self_won = false;
                    }
                }
                else if (data.type === "turn_change") {
                    this.my_turn = data.is_your_turn;
                }
            });
        },
        setGameId(game_id: string) {
            this.game_id = game_id;
        },
        setOtherPlayerStatus(status: "not-present" | "present" | "ready" | "playing") {
            this.other_player_status = status;
        },
        startPlacingShip(ship: "carrier" | "battleship" | "cruiser" | "submarine" | "destroyer") {
            this.currentShip = ship;
            const ship_ = this.ships.find(s => s.name === ship);
            if (ship_) {
                ship_.placed = false;
            }
        },
        placeShip(x: number, y: number, direction: "horizontal" | "vertical") {
            this.requestRunning = true;
            this.connection?.placeShip(this.currentShip!, x, y, direction).then(response => {
                console.log(response)
                if (response.status === "OK") {
                    const ship = this.ships.find(s => s.name === this.currentShip);
                    if (ship) {
                        ship.placed = true;
                        ship.position = { x, y };
                        ship.direction = direction;
                    }
                    this.currentShip = undefined;
                }
                else {
                    this.showToast("Nie można położyć tu statku", "error", 3000);
                }
                this.requestRunning = false;
            });

        },
        setOwnStatus(status: "present" | "ready" | "playing") {
            this.own_status = status;
            this.phase = "waiting-for-other-player";
        },
        createNewGame() {
            this.requestRunning = true;
            this.connection?.createNewGame().then(response => {
                this.game_id = response.game_id;
                this.phase = "placing-ships";
                this.requestRunning = false;
            });
        },
        joinGame(game_id: string) {
            this.requestRunning = true;
            this.connection?.joinGame(game_id).then(response => {
                if (response.status === "OK") {
                    this.game_id = game_id;                    
                    this.phase = "placing-ships";
                    this.other_player_status = "present";
                }
                else {
                    this.showToast("Nie udało się dołączyć do gry", "error", 3000);
                }
                this.requestRunning = false;
            });
        },
        sendReady() {
            this.requestRunning = true;
            this.connection?.sendReady().then(_response => {
                this.requestRunning = false;
            });
        },
        shoot(x: number, y: number) {
            this.requestRunning = true;
            this.connection?.shoot(x, y).then(response => {
                if (response.status === "OK") {
                    const { hit, is_game_won } = response;
                    const cell = `${x};${y}`;
                    if (cell in this.enemyCellStatus) {
                        (this.enemyCellStatus as any)[cell] = hit ? "hit" : "miss";
                    }
                    if (is_game_won) {
                        this.phase = "game-over";
                        this.self_won = true;
                    }
                }
                else {
                    this.showToast("Nie udało się strzelić", "error", 3000);
                }
                this.requestRunning = false;
            });
        },
        showToast(text: string, type: "info" | "error", duration: number) {
            const toast = { text, type };
            this.toasts.push(toast);
            setTimeout(() => {
                this.toasts = this.toasts.filter(t => t.text !== text && t.type !== type);
            }, duration);
        }
    },

    getters: {
        showLoadingScreen(): boolean {
            return !this.connection || this.requestRunning;
        }
    }
});