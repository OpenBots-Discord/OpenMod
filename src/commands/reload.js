const Command = require('../structures/Command');
const loadCommands = require('../utils/loadCommands');
const loadListeners = require('../utils/loadListeners');
const loadLocales = require('../utils/loadLocales');

module.exports = class extends Command {
    constructor() {
        super('reload', {});
    }

    async run(message, args, locales) {
        // TODO: сделать возможность перезагружать определенную команду или слушатели или группу (команды, листенеры или локали)
        await loadCommands(message.client, '../commands/');
        await loadListeners(message.client, '../listeners/');
        await loadLocales(message.client, '../locales/');
        console.log(message.client.commands);
    }
};
