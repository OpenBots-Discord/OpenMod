const { Collection } = require('discord.js');
const cooldown = new Collection();

class CommandExecutor {
    constructor(message, client) {
        this.message = message;
        this.client = client;
    }

    async runCommand() {
        const prefix = this.client.prefix;

        // Commands will not be working if the prefix is
        // incorrect or the message was sent in DM
        if (this.client.cache.reloading) return;
        if (!this.message.content.startsWith(prefix)) return;
        if (this.message.author.bot) return;
        if (this.message.channel.type === 'dm' || !this.message.guild) return;

        const [cmd, ...args] = this.message.content
            .slice(prefix.length)
            .trim()
            .split(/ +/g);

        const command =
            this.client.commands.get(cmd) ||
            this.client.commands.get(this.client.aliases.get(cmd));

        if (
            cooldown.has(this.message.author.id) &&
            cooldown.get(this.message.author.id) === command?.name
        )
            return this.message.react('⏱️').catch();

        if (command) {
            try {
                // TODO: определение языка (через бд или регион сервера)
                await command.run(this.message, args, this.client.locales.en);
                this.client.emit('command', command.name, this.message);
            } catch (error) {
                this.client.emit(
                    'commandError',
                    command.name,
                    error,
                    this.message
                );
            }

            cooldown.set(this.message.author.id, command.name);
            setTimeout(
                () => cooldown.delete(this.message.author.id),
                command.cooldown * 1000
            );
        }
    }
}

module.exports = CommandExecutor;
