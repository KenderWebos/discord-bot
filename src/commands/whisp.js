const {SlashCommandBuilder} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('whisp')
    .setDescription('Whisp a message to a user.')
    .addUserOption((option) =>
      option
        .setName('user')
        .setRequired(true)
        .setDescription('The user to whisp the message to.')
    )
    .addStringOption((option) =>
      option
        .setName('message')
        .setRequired(true)
        .setDescription('The message to whisp.')
    ),

  async execute(interaction, client) {
    const user = interaction.options.getUser('user');
    const message = interaction.options.getString('message');
    await user.send(message);
    await interaction.reply({
      content: `Whisped ${message} to ${user.username}`,
      emhemeral: true,
    });
  },
};
