module.exports = {
  name: 'interactionCreate',
  async execute(interaction, client) {
    if (!interaction.isChatInputCommand()) return;
    const {commands} = client;
    const {commandName} = interaction;
    const command = commands.get(commandName);
    if (!command) return;

    try {
      await command.execute(interaction, client);
    } catch (e) {
      console.error(e);
      await interaction.reply({
        content: 'An error occurred while executing this command.',
        ephemeral: true,
      });
    }
  },
};
