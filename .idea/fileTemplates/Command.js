const Command = require('../structures/Command');

module.exports = class extends Command {
    constructor() {
        super('$NAME', {});
    }

    async run(message, args, locales) {}
};
