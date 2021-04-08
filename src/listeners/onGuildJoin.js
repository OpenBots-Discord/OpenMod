const Listener = require('../structures/Listener');
const GuildModel = require('../models/GuildModel');

module.exports = class extends Listener {
    constructor() {
        super('onGuildJoin', 'guildCreate');
    }

    async run(client, guild) {
        const model = new GuildModel({
            guildID: guild.id,
            locale: 'en',
            prefix: 'm.',
        });
        await model.save();
    }
};
