const path = require('path');
const fs = require('fs').promises;
const Command = require('../structures/Command');

module.exports = async function loadCommands(client, dir, reset = false) {
    if (reset) {
        client.commands.clear();
        client.aliases.clear();
    }
    // fetching all the files in a directory (wholesome 100 reddit big chungus)
    const filesPath = path.join(__dirname, dir);
    const files = await fs.readdir(filesPath);

    for (const file of files) {
        const filePath = path.join(filesPath, file);
        const lstat = await fs.lstat(filePath);

        // recursive  loading
        if (lstat.isDirectory())
            await loadCommands(client, path.join(dir, file));
        if (file.endsWith('.js')) {
            let commandPrototype = require(filePath);

            // if the command is instance of Command structure
            // we add this into the listeners collection and
            if (commandPrototype.prototype instanceof Command) {
                const command = new commandPrototype();
                console.log(client.commands.set(command.name, command));
                command.aliases.forEach((value) => {
                    client.aliases.set(value, command.name);
                });
            }
        }
    }
};
