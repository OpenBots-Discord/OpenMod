const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onCommand', 'command');
    }

    async run(client, command, message) {
        const timestamp = message.createdAt.toLocaleString('us');
        const user =
            message.author.username + '#' + message.author.discriminator;
        const guild = message.guild.name;

        console.log(`[${timestamp}] ${user} (${guild}) -> ${command.name}`);
    }
};
