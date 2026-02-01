import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import random
import requests
import html

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Diccionario de emojis y mensajes
ELEMENTOS = {
    "fuego": {"emoji": "🔥", "mensaje_empate": "¡Todo está en llamas! 🔥🔥"},
    "agua": {"emoji": "💧", "mensaje_empate": "¡Todo está inundado! 💧💧"},
    "nieve": {"emoji": "❄️", "mensaje_empate": "¡Todo se congela! ❄️❄️"}
}

class TriviaView(View):
    def __init__(self, correct_answer):
        super().__init__(timeout=60)
        self.correct_answer = correct_answer

print("Iniciando bot...")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def cat(ctx):
    try:
        # Hacer la petición a la API
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                cat_url = data[0]['url']
                
                # Crear embed para mostrar la imagen del gato
                embed = discord.Embed(
                    title="🐱 ¡Aquí tienes tu gato! 🐱",
                    color=discord.Color.orange()
                )
                embed.set_image(url=cat_url)
                embed.set_footer(text="Powered by The Cat API")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Lo siento, no pude encontrar una imagen de gato 😿")
        else:
            await ctx.send("Lo siento, hubo un error al obtener la imagen del gato 😿")
    except Exception as e:
        print(f"Error en comando cat: {e}")
        await ctx.send("Lo siento, hubo un error al obtener la imagen del gato 😿")

@bot.tree.command(name="jugar", description="Juega a Fuego, Nieve y Agua")
async def jugar(interaction: discord.Interaction, opcion: str):
    try:
        opciones = ["fuego", "nieve", "agua"]
        if opcion.lower() not in opciones:
            await interaction.response.send_message("Por favor, elige una opción válida: fuego, nieve o agua.", ephemeral=True)
            return

        bot_choice = random.choice(opciones)
        resultado = determinar_ganador(opcion.lower(), bot_choice)
        
        # Crear embed para la respuesta
        embed = discord.Embed(
            title="🎮 Fuego, Nieve y Agua 🎮",
            color=discord.Color.blue()
        )
        
        # Añadir campos al embed
        embed.add_field(
            name="Tu elección",
            value=f"{ELEMENTOS[opcion.lower()]['emoji']} {opcion.capitalize()}",
            inline=True
        )
        embed.add_field(
            name="Elección del bot",
            value=f"{ELEMENTOS[bot_choice]['emoji']} {bot_choice.capitalize()}",
            inline=True
        )
        embed.add_field(
            name="Resultado",
            value=resultado,
            inline=False
        )
        
        # Añadir footer
        embed.set_footer(text="¡Gracias por jugar! 🎲")
        
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error en comando jugar: {e}")
        await interaction.response.send_message("Hubo un error al ejecutar el comando.", ephemeral=True)

def determinar_ganador(jugador, bot):
    if jugador == bot:
        return f"**¡Empate!** {ELEMENTOS[jugador]['mensaje_empate']}"
    elif (jugador == "fuego" and bot == "nieve") or (jugador == "nieve" and bot == "agua") or (jugador == "agua" and bot == "fuego"):
        return f"**¡Ganaste!** {ELEMENTOS[jugador]['emoji']} vence a {ELEMENTOS[bot]['emoji']}"
    else:
        return f"**¡Perdiste!** {ELEMENTOS[bot]['emoji']} vence a {ELEMENTOS[jugador]['emoji']}"

@bot.tree.command(name="help", description="Muestra información sobre los comandos disponibles")
async def help(interaction: discord.Interaction):
    try:
        embed = discord.Embed(title="Comandos del Bot", description="Aquí tienes una lista de los comandos disponibles:", color=discord.Color.blue())
        embed.add_field(name="!ping", value="Responde con 'Pong!'", inline=False)
        embed.add_field(name="!cat", value="Muestra una imagen aleatoria de gato", inline=False)
        embed.add_field(name="/jugar [opcion]", value="Juega a Fuego, Nieve y Agua. Opciones: fuego, nieve, agua", inline=False)
        embed.add_field(name="/trivia", value="Pregunta de trivia aleatoria con opciones múltiples", inline=False)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error en comando help: {e}")
        await interaction.response.send_message("Hubo un error al ejecutar el comando.", ephemeral=True)

@bot.tree.command(name="trivia", description="Pregunta de trivia aleatoria con opciones múltiples")
async def trivia(interaction: discord.Interaction):
    try:
        response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
        if response.status_code != 200:
            await interaction.response.send_message("Lo siento, no pude obtener una pregunta de trivia en este momento.", ephemeral=True)
            return

        data = response.json()
        if data['response_code'] != 0 or not data['results']:
            await interaction.response.send_message("No hay preguntas disponibles.", ephemeral=True)
            return

        result = data['results'][0]
        question = html.unescape(result['question'])
        correct_answer = html.unescape(result['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in result['incorrect_answers']]

        options = [correct_answer] + incorrect_answers
        random.shuffle(options)

        embed = discord.Embed(
            title="🧠 Pregunta de Trivia 🧠",
            description=question,
            color=discord.Color.green()
        )
        embed.set_footer(text="Elige una opción haciendo clic en el botón correspondiente.")

        view = TriviaView(correct_answer)

        for option in options:
            button = Button(label=option, style=discord.ButtonStyle.primary)
            async def button_callback(interaction, button=button, option=option):
                if option == view.correct_answer:
                    await interaction.response.send_message("¡Correcto! 🎉 Bien hecho.", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Incorrecto. La respuesta correcta era: **{view.correct_answer}**. ¡No te desanimes, sigue intentando! 😄", ephemeral=True)
            button.callback = button_callback
            view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view)
    except Exception as e:
        print(f"Error en comando trivia: {e}")
        await interaction.response.send_message("Hubo un error al ejecutar el comando.", ephemeral=True)

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}") 