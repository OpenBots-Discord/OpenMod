const GuildModel = require('../models/GuildModel');
const CooldownManager = require('./CooldownManager');
const { Collection, Team, User } = require('discord.js');

class CommandExecutor {
    constructor(message, client) {
        this.message = message;
        this.client = client;
    }

    async runCommand() {
        const data = await GuildModel.getData(this.message.guild.id);
        console.log(data);
        const prefix = data.prefix;
        const locale = data.locale;
        const [cmd, ...args] = this.message.content
            .slice(prefix.length)
            .trim()
            .split(/ +/g);
        const command =
            this.client.commands.get(cmd) ||
            this.client.commands.get(this.client.aliases.get(cmd));

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

        try {
            this.client.emit('command', command, this.message);

            const ok = await command.run(
                this.message,
                args,
                this.client.locales[data.locale]
            );

            if (ok) this.client.emit('commandSuccess', command, this.message);
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

module.exports = CommandExecutor;
