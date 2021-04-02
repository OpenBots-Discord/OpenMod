const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onCommand', 'command');
    }

    async run(client, commandName, message) {
        // TODO: привести в порядок
        console.log(commandName, message.author.username);
    }
};
