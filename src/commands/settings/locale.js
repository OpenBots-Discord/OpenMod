const Command = require('../../structures/Command');
const GuildModel = require('../../models/GuildModel');
const getLocales = require('../../utils/getLocales');

module.exports = class extends Command {
    constructor() {
        super('locale', {});
    }

    async run(message, args, locales) {
        const availableLocales = await getLocales('../locales/');
        if (availableLocales.includes(args[0])) {
            return GuildModel.setData(message.guild.id, { locale: args[0] });
        }
    }
};
