const mongoose = require('mongoose');
const config = require('../config.json');

let GuildModel = mongoose.model(
    'guild_settings',
    new mongoose.Schema(
        {
            guildID: {
                type: String,
                required: true,
                unique: true,
                index: true,
            },
            prefix: {
                type: String,
                default: config.default_prefix,
            },
            locale: {
                type: String,
                default: config.default_locale,
            },
        },
        { _id: false }
    )
);

GuildModel.setData = async function (guildID, data) {
    return await this.findOneAndUpdate(
        { guildID: guildID },
        { $set: data },
        { new: true }
    );
};

GuildModel.getData = async function (guildID) {
    return GuildModel.findOne({ guildID: guildID }).exec();
};

module.exports = GuildModel;
