const mongoose = require('mongoose');
const getLocales = require('../utils/getLocales');

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
                default: 'm.',
            },
            locale: {
                type: String,
                default: 'en',
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

GuildModel.getData = function (guildID) {
    return GuildModel.findOne({ guildID: guildID }).exec();
};

module.exports = GuildModel;
