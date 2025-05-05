if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const {Routes, REST} = require('discord.js');

const rest = new REST({version: '10'}).setToken(process.env.DISCORD_TOKEN);

rest.put(Routes.applicationCommands(process.env.APPLICATION_ID), {body: []});
