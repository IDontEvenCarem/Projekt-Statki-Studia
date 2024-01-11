import { defineStore } from "pinia";
import { CommunicationApi } from "./comms";

type ShipName = "carrier" | "battleship" | "cruiser" | "submarine" | "destroyer";

export const useStore = defineStore('mainStore', {
    state: () => ({
        connection: undefined as undefined | CommunicationApi,
        game_id: undefined as string | undefined,
        phase: "main-menu" as "main-menu" | "placing-ships" | "waiting-for-other-player" | "playing" | "game-over",
        own_status: "present" as "present" | "ready" | "playing",
        other_player_status: "not-present" as "not-present" | "present" | "ready" | "playing",
        ships: [
            { name: "carrier" as ShipName, size: 5, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "battleship" as ShipName, size: 4, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "cruiser" as ShipName, size: 3, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "submarine" as ShipName, size: 3, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
            { name: "destroyer" as ShipName, size: 2, placed: false, position: { x: 0, y: 0 }, direction: "horizontal" as "horizontal" | "vertical" },
        ],
        currentShip: undefined as undefined | "carrier" | "battleship" | "cruiser" | "submarine" | "destroyer",
        requestRunning: false,
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
                if (response.status === "OK") {
                    const ship = this.ships.find(s => s.name === this.currentShip);
                    if (ship) {
                        ship.placed = true;
                        ship.position = { x, y };
                        ship.direction = direction;
                    }
                    this.currentShip = undefined;
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
                this.requestRunning = false;
            });
        },
        sendReady() {
            this.requestRunning = true;
            this.connection?.sendReady().then(_response => {
                this.requestRunning = false;
            });
        }
    },

    getters: {
        showLoadingScreen(): boolean {
            return !this.connection || this.requestRunning;
        }
    }
});