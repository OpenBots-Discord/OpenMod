const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onCommandError', 'commandError');
    }

    async run(client, command, error, message) {
        await message.react('<:OB_mark_NO:761645981917773826>');
        console.error(`\n${error.stack}\n`);
        await message.channel.send('```\n' + error.stack + '```');
    }
};
