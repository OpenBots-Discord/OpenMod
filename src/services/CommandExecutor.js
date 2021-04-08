const GuildModel = require('../models/GuildModel');
const CooldownManager = require('./CooldownManager');
const { Team, User } = require('discord.js');

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
        const [commandName, ...args] = this.message.content
            .slice(prefix.length)
            .trim()
            .split(/ +/g);
        const command =
            this.client.commands.get(commandName) ||
            this.client.commands.get(this.client.aliases.get(commandName));

        if (!command) return;
        if (!this.message.content.startsWith(prefix)) return;
        if (this.message.author.bot) return;
        if (this.message.channel.type === 'dm' || !this.message.guild) return;

        // TODO: сделать отдельный пермишн менеджер (???????)
        if (!this.message.guild.me.permissions.has(command.botPermissions)) {
            // FIXME                   VVVVVVVVVVVVVVVVVVVV
            return this.message.reply('bruh i have no perms');
        }

        if (!this.message.member.permissions.has(command.userPermissions)) {
            // FIXME                   VVVVVVVVVVVVVVVVVVVV
            return this.message.reply(`bruh u have no perms`);
        }

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
