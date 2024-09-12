const {SlashCommandBuilder} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('hola')
    .setDescription('Replies with HolaMundo! ✌️'),
  async execute(interaction, client) {
    await interaction.reply('HolaMundo! ✌️');
  },
};
