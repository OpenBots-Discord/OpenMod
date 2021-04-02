class Listener {
    constructor(name, emitter) {
        this.name = name;
        this.emitter = emitter;
    }

    async run() {
        throw new Error('You need to implement the async method run!');
    }
}

module.exports = Listener;
