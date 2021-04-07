const Command = require('../structures/Command');

module.exports = class extends Command {
    constructor() {
        super('eval', {
            botOwnerOnly: true,
            aliases: ['e'],
        });
    }

    async run(message, args, locales) {
        const util = require('util');
        let code = args.join(' '),
            isAsync = false;

        try {
            if (!code) return message.reply('maybe some code? =)');
            code = code.replace(/(```(js)?)?/g, '');

            if (code.includes('await')) isAsync = true;
            if (isAsync) code = '(async () => {' + code + '})()';

            let before = process.hrtime.bigint();
            let executed = eval(code);

            if (util.types.isPromise(executed)) executed = await executed;
            let after = process.hrtime.bigint();

            if (typeof executed !== 'string') executed = util.inspect(executed);
            if (['undefined', 'null'].some((r) => executed === r))
                executed = `Empty response: ${executed}`;

            if (executed.length >= 1940) {
                message.channel.send("⚠️ Response was DM'ed");
                return message.member.send(executed, {
                    split: '\n',
                    code: 'js',
                });
            }

            executed = `Executed for ${(
                parseInt(after - before) / 1000000
            ).toFixed(3)} ms.\n${executed}`;
            message.reply(`\`\`\`js\n${clean(executed)}\`\`\``);
        } catch (error) {
            message.reply(`\`\`\`js\n${error}\`\`\``);
        }

        function clean(text) {
            return text
                .replace(/`/g, '`' + String.fromCharCode(8203))
                .replace(/@/g, '@' + String.fromCharCode(8203));
        }
    }
};
