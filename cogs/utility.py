import discord
from discord.ext import commands
from discord import app_commands
from gtts import gTTS
import asyncio
import threading
import functools

def generate_tts(text, filename="speech.mp3"):
    tts = gTTS(text=text, lang='es')
    tts.save(filename)

def save_tts(text, filename):
    tts = gTTS(text=text, lang='es')
    tts.save(filename)

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Desconectado del canal de voz.")
        else:
            await ctx.send("No estoy conectado a un canal de voz.")

    @app_commands.command(name="join", description="Conecta el bot al canal de voz del usuario")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            return await interaction.response.send_message("¡Debes estar en un canal de voz!", ephemeral=True)

        if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
            return await interaction.response.send_message("Ya estoy en un canal de voz.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        channel = interaction.user.voice.channel
        filename = "hello.mp3"

        try:
            vc = await channel.connect()

            threading.Thread(target=generate_tts, args=("¡Hola mundo!", filename)).start()
            await asyncio.sleep(1.5)

            if vc.is_connected():
                vc.play(discord.FFmpegPCMAudio(filename))

            await interaction.followup.send(f"¡Conectado exitosamente a {channel.name}!")

        except Exception as e:
            print(f"Error en join: {e}")
            await interaction.followup.send("Hubo un problema al intentar conectar.")

    @app_commands.command(name="leave", description="Desconecta el bot del canal de voz")
    async def leave_slash(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_connected():
            await vc.disconnect()
            await interaction.response.send_message("Desconectado del canal de voz.", ephemeral=True)
        else:
            await interaction.response.send_message("No estoy conectado a un canal de voz.", ephemeral=True)

    @app_commands.command(name="decir", description="Hace que el bot diga algo en voz alta")
    @app_commands.describe(texto="Lo que quieres que el bot diga")
    async def decir(self, interaction: discord.Interaction, texto: str):
        vc = interaction.guild.voice_client
        if not vc or not vc.is_connected():
            return await interaction.response.send_message("Primero usa /join para conectarme.", ephemeral=True)

        await interaction.response.defer()

        try:
            filename = f"tts_{interaction.guild.id}.mp3"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, functools.partial(save_tts, texto, filename))

            if vc.is_playing():
                vc.stop()

            vc.play(discord.FFmpegPCMAudio(filename))
            await interaction.followup.send(f"Diciendo: *{texto}*")

        except Exception as e:
            print(f"Error al hablar: {e}")
            await interaction.followup.send("No pude reproducir el audio.")

    @app_commands.command(name="help", description="Muestra información sobre los comandos disponibles")
    async def help(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Comandos del Bot", description="Aquí tienes una lista de los comandos disponibles:", color=discord.Color.blue())
            embed.add_field(name="!ping", value="Responde con 'Pong!'", inline=False)
            embed.add_field(name="!leave", value="Desconecta el bot del canal de voz", inline=False)
            embed.add_field(name="!cat", value="Muestra una imagen aleatoria de gato", inline=False)
            embed.add_field(name="/join", value="Conecta el bot al canal de voz del usuario", inline=False)
            embed.add_field(name="/leave", value="Desconecta el bot del canal de voz", inline=False)
            embed.add_field(name="/decir [texto]", value="Hace que el bot diga algo en voz alta", inline=False)
            embed.add_field(name="/jugar [opcion]", value="Juega a Fuego, Nieve y Agua. Opciones: fuego, nieve, agua", inline=False)
            embed.add_field(name="/trivia", value="Pregunta de trivia aleatoria con opciones múltiples", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error en comando help: {e}")
            await interaction.response.send_message("Hubo un error al ejecutar el comando.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))