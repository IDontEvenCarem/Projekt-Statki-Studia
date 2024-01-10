import { defineStore } from "pinia";

export const useStore = defineStore('mainStore', {
    state: () => ({
        game_id: undefined as string | undefined,
        other_player_status: "not-present" as "not-present" | "present" | "ready" | "playing",
    }),

    actions: {
        setGameId(game_id: string) {
            this.game_id = game_id;
        },
        setOtherPlayerStatus(status: "not-present" | "present" | "ready" | "playing") {
            this.other_player_status = status;
        }
    }
});