class Command {
    constructor(name, options) {
        this.name = name;
        this.group = options.group || '';
        this.description = options.description || 'N/A';
        this.usage = options.usage || 'N/A';
        this.aliases = options.aliases || [];
        this.cooldown = options.cooldown || 0;
    }

    async run(message, args, locales) {
        throw new Error('You need to implement the async method run!');
    }
}

module.exports = Command;
