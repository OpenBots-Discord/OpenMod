const DiscordClient = require('discord.js').Client;
const { Collection } = require('discord.js');
const loadListeners = require('../utils/loadListeners');
const loadCommands = require('../utils/loadCommands');
const loadLocales = require('../utils/loadLocales');
const mongoose = require('mongoose');

class Client extends DiscordClient {
    constructor(options) {
        super(options);

        this.config = require('../config.json');
        mongoose
            .connect(this.config.mongo_url, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
                useFindAndModify: false,
            })
            .then(() => (this.mongo = mongoose.connection));
        this.listeners = new Collection();
        this.commands = new Collection();
        this.aliases = new Collection();

        this.locales = {};
        this.prefix = '!';
    }

    async launch() {
        await loadLocales(this, '../locales/');
        await loadListeners(this, '../listeners/');
        await loadCommands(this, '../commands/');

        await this.login(this.config.token);
    }
}

module.exports = Client;
