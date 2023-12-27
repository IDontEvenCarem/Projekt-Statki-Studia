export class CommunicationApi extends EventTarget {
    #ws: WebSocket;
    #awaiters = new Map<string, (data: any) => void>();

    constructor(url: string) {
        super();
        this.#ws = new WebSocket(url);
        this.#ws.addEventListener('message', (event) => {
            this.dispatchEvent(new CustomEvent('message', { detail: event.data }));
            const data = JSON.parse(event.data);
            const awaiter = this.#awaiters.get(data.id);
            if (awaiter) {
                awaiter(data);
                this.#awaiters.delete(data.id);
            }
        });
    }
    
    send(message: string) {
        this.#ws.send(message);
    }

    close() {
        this.#ws.close();
    }    

    async joinGame(name: string) {
        return await this.sendAndWait({ type: 'join', name });
    }

    async createNewGame(name: string, is_public: boolean) {
        return await this.sendAndWait({ type: 'create', name, public: is_public });
    }

    async startGame() {
        return await this.sendAndWait({ type: 'start' });
    }

    async sendAndWait(message: any) {
        return new Promise((resolve) => {
            const id = Math.random().toString();
            this.#awaiters.set(id, resolve);
            this.send(JSON.stringify({ ...message, id }));
        });
    }
}