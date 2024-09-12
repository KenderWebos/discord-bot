const { SlashCommandBuilder } = require('discord.js');
const axios = require('axios');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('dolar')
    .setDescription('Retorna el precio del dólar en CLP'),
  async execute(interaction, client) {
    try {
      const response = await axios.get('https://api.exchangerate-api.com/v4/latest/USD'); // Ejemplo de API, reemplaza con la tuya
      const rate = response.data.rates.CLP;
      await interaction.reply(`El precio del dólar en CLP es ${rate}`);
    } catch (error) {
      await interaction.reply('No se pudo obtener el precio del dólar.');
    }
  },
};
