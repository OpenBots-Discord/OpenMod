const { Collection } = require('discord.js');

class CooldownManager {
    static cooldown = new Collection();

    static setCooldown(seconds, invoker, event) {
        CooldownManager.cooldown.set(invoker, event);
        setTimeout(
            () => CooldownManager.cooldown.delete(invoker),
            seconds * 1000
        );
    }

    static hasCooldown(invoker, event) {
        return (
            CooldownManager.cooldown.has(invoker) &&
            CooldownManager.cooldown.get(invoker) === event
        );
    }
}

module.exports = CooldownManager;
