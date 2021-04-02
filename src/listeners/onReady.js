const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onReady', 'ready');
    }

    async run(client) {
        console.log('Bot is ready!');
    }
};
