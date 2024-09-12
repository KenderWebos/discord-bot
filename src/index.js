if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const fs = require('fs');
const path = require('path');
const {Client, GatewayIntentBits, Partials, Collection} = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.DirectMessageTyping,
    GatewayIntentBits.DirectMessageReactions,
  ],
  partials: [Partials.Channel, Partials.Message, Partials.Reaction],
});

client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
const eventsPath = path.join(__dirname, 'events');

const commandFiles = fs
  .readdirSync(commandsPath)
  .filter((file) => file.endsWith('.js'));

const eventFiles = fs
  .readdirSync(eventsPath)
  .filter((file) => file.endsWith('.js'));

commandFiles.forEach((file) => {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  client.commands.set(command.data.name, command);
});

eventFiles.forEach((file) => {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  if (event.once) {
    client.once(
      event.name,
      async (interaction) => await event.execute(interaction, client)
    );
  } else {
    client.on(
      event.name,
      async (interaction) => await event.execute(interaction, client)
    );
  }
});
client.login(process.env.DISCORD_TOKEN);
