const GuildModel = require('../models/GuildModel');
const CooldownManager = require('./CooldownManager');
const { Collection, Team, User } = require('discord.js');

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
        // TODO: сделать пермишн чекер впринципе
        if (command.botOwnerOnly) {
            const appOwner = this.client.owner;
            if (appOwner instanceof Team) {
                const ownerIDs = Team.members.values().map((v) => v.id);

                if (appOwner.ownerID !== this.message.author.id) return;
                if (!this.message.author.id in ownerIDs) return;
            } else if (appOwner instanceof User) {
                if (appOwner.id !== this.message.author.id) return;
            }
        }

        if (CooldownManager.hasCooldown(this.message.author.id, command.name))
            return await this.message.react('⏱️').catch();

        if (command) {
            const data = await GuildModel.getData(this.message.guild.id);
            try {
                this.client.emit('command', command, this.message);

                const ok = await command.run(
                    this.message,
                    args,
                    this.client.locales[data.locale]
                );

                if (ok)
                    this.client.emit('commandSuccess', command, this.message);
            } catch (error) {
                this.client.emit('commandError', command, error, this.message);
            }

            CooldownManager.setCooldown(
                command.cooldown,
                this.message.author.id,
                command.name
            );
        }
    }
}

module.exports = CommandExecutor;
