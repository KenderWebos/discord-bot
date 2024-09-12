if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const fs = require('node:fs');
const path = require('node:path');
const {Routes, REST} = require('discord.js');

const rest = new REST({version: '10'}).setToken(process.env.DISCORD_TOKEN);
const commands = [];
const commandsPath = path.resolve(__dirname, '../commands');
const commandFiles = fs
  .readdirSync(commandsPath)
  .filter((file) => file.endsWith('.js'));

commandFiles.forEach((file) => {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  commands.push(command.data.toJSON());
});

rest
  .put(Routes.applicationCommands(process.env.APPLICATION_ID), {
    body: commands,
  })
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })