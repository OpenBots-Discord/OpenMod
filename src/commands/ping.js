const Command = require('../structures/Command');

module.exports = class extends Command {
    constructor() {
        super('ping', {
            aliases: ['pinggg'],
            cooldown: 3,
        });
    }

    async run(message, args, locales) {
        return await message.reply(locales.ping);
    }
};
