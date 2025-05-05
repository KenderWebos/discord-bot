const {SlashCommandBuilder} = require('discord.js');

function rockPaperScissors({name1, choice1}, {name2, choice2}) {
  if (choice1 === choice2) {
    return 'Tie!';
  }

  switch (choice1) {
    case 'rock':
      if (choice2 === 'scissors') {
        return name1 + ' wins with ' + choice1;
      }
      return name2 + ' wins with ' + choice1;
    case 'paper':
      if (choice2 === 'rock') {
        return name1 + ' wins with ' + choice1;
      }
      return name2 + ' wins with ' + choice2;
    case 'scissors':
      if (choice2 === 'paper') {
        return name1 + ' wins with ' + choice1;
      }
      return name2 + ' wins with ' + choice2;
    default:
      return 'Invalid input!';
  }
}

module.exports = {
  data: new SlashCommandBuilder()
    .setName('cachipun')
    .setDescription('Juega a piedra, papel o tijeras con el bot.')
    .addStringOption((option) =>
      option
        .setName('choice')
        .setDescription('Selecciona una opción')
        .setRequired(true)
        .addChoices(
          {
            name: 'rock',
            value: 'rock',
          },
          {
            name: 'paper',
            value: 'paper',
          },
          {
            name: 'scissors',
            value: 'scissors',
          }
        )
    ),
  async execute(interaction, client) {
    const opciones = ['rock', 'paper', 'scissors'];
    const choice = interaction.options.getString('choice');
    const botChoice = Math.floor(Math.random() * 3);
    const botChoiceString = opciones[botChoice];
    await interaction.reply(
      rockPaperScissors(
        {name1: 'You', choice1: choice},
        {name2: 'Bot', choice2: botChoiceString}
      )
    );
  },
};
