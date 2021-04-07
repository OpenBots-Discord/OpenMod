const GuildModel = require('../models/GuildModel');
const { Collection, Team, User } = require('discord.js');
const cooldown = new Collection();

class CommandExecutor {
    constructor(message, client) {
        this.message = message;
        this.client = client;
    }

    async runCommand() {
        const prefix = this.client.prefix;
        const [cmd, ...args] = this.message.content
            .slice(prefix.length)
            .trim()
            .split(/ +/g);
        const command =
            this.client.commands.get(cmd) ||
            this.client.commands.get(this.client.aliases.get(cmd));

        // Commands will not be working if the prefix is
        // incorrect or the message was sent in DM
        if (!command) return;
        if (!this.message.content.startsWith(prefix)) return;
        if (this.message.author.bot) return;
        if (this.message.channel.type === 'dm' || !this.message.guild) return;

        // TODO: сделать отдельный пермишн чекер
        if (command.botOwnerOnly) {
            const appOwner = this.client.owner;
            if (appOwner instanceof Team) {
                let found = false;
                Team.members.forEach((member) => {
                    if (member.id === this.message.author.id) {
                        found = true;
                    }
                });

                found = found || appOwner.ownerID === this.message.author.id;
                if (!found) return;
            } else if (appOwner instanceof User) {
                if (appOwner.id !== this.message.author.id) return;
            }
        }

        if (
            cooldown.has(this.message.author.id) &&
            cooldown.get(this.message.author.id) === command?.name
        )
            return await this.message.react('⏱️').catch();

        if (command) {
            const props = await GuildModel.getProps(this.message.guild.id);
            try {
                this.client.emit('command', command, this.message);
                const ok = await command.run(
                    this.message,
                    args,
                    this.client.locales[props.locale]
                );
                if (ok)
                    this.client.emit('commandSuccess', command, this.message);
            } catch (error) {
                this.client.emit('commandError', command, error, this.message);
            }

            cooldown.set(this.message.author.id, command);
            setTimeout(
                () => cooldown.delete(this.message.author.id),
                command.cooldown * 1000
            );
        }
    }
}

module.exports = CommandExecutor;
