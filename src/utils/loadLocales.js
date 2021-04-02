const fs = require('fs').promises;
const path = require('path');

module.exports = async function loadLocales(client, dir) {
    client.locales = {};

    const filesPath = path.join(__dirname, dir);
    const files = await fs.readdir(filesPath);

    for (const file of files) {
        const filePath = path.join(filesPath, file);
        const lstat = await fs.lstat(filePath);
        const fileName = path.parse(filePath).name;

        if (!lstat.isDirectory() && file.endsWith('.json')) {
            client.locales[fileName] = require(filePath);
        }
    }
};
