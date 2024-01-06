type Message = {
    type: string;
    request_id: string;
    [key: string]: any;    
}

export class CommunicationApi extends EventTarget {
    #ws: WebSocket;
    #awaiters = new Map<string, ((data: any) => void)[]>();

    constructor(url: string) {
        super();
        this.#ws = new WebSocket(url);
        this.#ws.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'response') {
                const awaiter = this.#awaiters.get(data.request_id);
                if (awaiter) {
                    for (const awaiter_ of awaiter) awaiter_(data);
                    this.#awaiters.delete(data.request_id);
                }
            }

            const event_ = new CustomEvent<Message>('message', { detail: data });
            this.dispatchEvent(event_);
        });
        this.#ws.addEventListener('close', () => {
            const event_ = new CustomEvent('error', { detail: 'Connection closed' });
            this.dispatchEvent(event_);
        });
        this.#ws.addEventListener('error', e => {           
            const msg = e instanceof Error ? e.message : e;
            const event_ = new CustomEvent('error', { detail: msg });
            this.dispatchEvent(event_);
        });
    }
    
    send(message: Object) {
        const request_id = Math.random().toString();
        const prepared_message = {
            ...message,
            request_id,
        };
        this.#ws.send(JSON.stringify(prepared_message));
        return request_id;
    }

    close() {
        this.#ws.close();
    }

    joinGame(name: string) {
        return this.sendAndWait({ type: 'join_game', name });
    }

    createNewGame() {
        return this.sendAndWait({ type: 'create_game' });
    }

    startGame() {
        return this.sendAndWait({ type: 'start' });
    }

    async sendAndWait(message: Object): Promise<any> {
        return new Promise((resolve) => {
            const request_id = this.send(message);
            const awaiter = this.#awaiters.get(request_id) ?? [];
            awaiter.push(resolve);
            this.#awaiters.set(request_id, awaiter);
        });
    }
}