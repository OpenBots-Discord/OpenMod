const Command = require('../structures/Command');
const GuildModel = require('../models/GuildModel');

module.exports = class extends Command {
    constructor() {
        super('prefix', {});
    }

    async run(message, args, locales) {
        return await GuildModel.setData(message.guild.id, { prefix: args[0] });
    }
};
