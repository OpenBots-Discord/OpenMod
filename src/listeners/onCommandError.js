const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onCommandError', 'commandError');
    }

    async run(client, commandName, error, message) {
        // TODO: это че вообще такое
        message.reply(
            `ебать произошла ошибка в команде ${commandName}\n\`\`\`${error.stack}\`\`\``
        );
    }
};
