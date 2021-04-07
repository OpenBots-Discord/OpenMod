const path = require('path');
const fs = require('fs').promises;

module.exports = async function getLocales(dir) {
    let locales = [];

    const filesPath = path.join(__dirname, dir);
    const files = await fs.readdir(filesPath);

    for (const file of files) {
        const filePath = path.join(filesPath, file);
        const lstat = await fs.lstat(filePath);
        const fileName = path.parse(filePath).name;

        if (!lstat.isDirectory() && file.endsWith('.json')) {
            locales.push(fileName);
        }
    }

    return locales;
};
