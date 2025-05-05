import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.tree.command(name="jugar", description="Juega a Fuego, Nieve y Agua")
async def jugar(interaction: discord.Interaction, opcion: str = discord.app_commands.Choice(name="opcion", choices=["fuego", "nieve", "agua"])):
    bot_choice = random.choice(["fuego", "nieve", "agua"])
    resultado = determinar_ganador(opcion, bot_choice)
    await interaction.response.send_message(f"Elegiste: {opcion.capitalize()}\nEl bot eligió: {bot_choice.capitalize()}\n{resultado}")

def determinar_ganador(jugador, bot):
    if jugador == bot:
        return "¡Empate!"
    elif (jugador == "fuego" and bot == "nieve") or (jugador == "nieve" and bot == "agua") or (jugador == "agua" and bot == "fuego"):
        return "¡Ganaste!"
    else:
        return "¡Perdiste!"

@bot.tree.command(name="help", description="Muestra información sobre los comandos disponibles")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Comandos del Bot", description="Aquí tienes una lista de los comandos disponibles:", color=discord.Color.blue())
    embed.add_field(name="/ping", value="Responde con 'Pong!'", inline=False)
    embed.add_field(name="/jugar [opcion]", value="Juega a Fuego, Nieve y Agua. Opciones: fuego, nieve, agua", inline=False)
    await interaction.response.send_message(embed=embed)

if __name__ == '__main__':
    bot.run(TOKEN) 