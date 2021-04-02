const Listener = require('../structures/Listener');

module.exports = class extends Listener {
    constructor() {
        super('$NAME', '$Event');
    }
    async run(client) {}
};
