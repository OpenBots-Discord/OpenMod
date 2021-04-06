const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('onCommandSuccess', 'commandSuccess');
    }

    async run(client, command, message) {
        await message.react('<:OB_mark_YES:761645863671955468>');
    }
};
