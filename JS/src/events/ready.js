module.exports = {
  name: 'ready',
  once: true,
  execute(interaction, client) {
    console.log(`Ready! Logged in as ${client.user.tag}`);
  },
};
