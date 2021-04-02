const DiscordClient = require('discord.js').Client;
const { Collection } = require('discord.js');
const loadListeners = require('../utils/loadListeners');
const loadCommands = require('../utils/loadCommands');
const loadLocales = require('../utils/loadLocales');

class Client extends DiscordClient {
    constructor(options) {
        super(options);

        this.config = require('../config.json');
        this.listeners = new Collection();
        this.commands = new Collection();
        this.aliases = new Collection();
        this.cache = {}; // it's needed to store some temporary data, so yeah
        this.locales = {};
        this.prefix = '!';
    }

    async launch() {
        await loadListeners(this, '../listeners/');
        await loadCommands(this, '../commands/');
        await loadLocales(this, '../locales/');

        await this.login(this.config.token);
    }
}

module.exports = Client;
