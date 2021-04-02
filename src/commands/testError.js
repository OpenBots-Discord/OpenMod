const Command = require('../structures/Command');

module.exports = class extends Command {
    constructor() {
        super('testError', {});
    }

    async run(message, args, locales) {
        return asdfasdfsadf;
    }
};
