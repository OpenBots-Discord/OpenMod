const Listener = require('../structures/Listener');
const CommandExecutor = require('../services/CommandExecutor');

module.exports = class extends Listener {
    constructor() {
        super('onMessage', 'message');
    }
    async run(client, message) {
        const executor = new CommandExecutor(message, client);
        return executor.runCommand();
    }
};
