import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction
import json
import os



with open('data.json') as f:
    data = json.load(f)

json_path = os.path.join(os.getcwd(), 'bosses.json')


    # Abrir el archivo JSON con codificación UTF-8
with open(json_path, 'r', encoding='utf-8') as f:
        bosses_data = json.load(f)
        
with open('weapons.json', 'r', encoding='utf-8') as f:
    weapons_data = json.load(f)

# Buscar un arma ignorando mayúsculas y guiones
def buscar_arma(weapon_name: str):
    weapon_name_lower = weapon_name.lower().replace("-", "").replace(" ", "")  # Quitar guiones y espacios
    for key in weapons_data:
        normalized_key = key.lower().replace("-", "").replace(" ", "")
        if weapon_name_lower == normalized_key:
            return weapons_data[key]
    return None


# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot
TOKEN = 'NTQ4MTM2MDU5MTE3MTA5MjY0.GmNDIW.PpdeulMicAGWbh0r0aRNGmz7O2wsnkkGcvxJJw'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
tree = bot.tree


# Ruta del banner
BANNER_URL = 'https://ibb.co/rxk4xVS'  # Asegúrate de usar una URL directa de imagen, no un enlace de página

# Mensaje de bienvenida
WELCOME_MESSAGE = """
¡Bienvenido al servidor de **Escape from Tarkov**!

🚀 **¡Estamos emocionados de tenerte con nosotros!** 🚀

Aquí encontrarás:
- **Canales de discusión**: Únete a nuestras charlas sobre estrategias, equipos y más.
- **Roles**: Obtén roles para acceder a canales específicos y destacarte en la comunidad.
- **Reglas del servidor**: Por favor, asegúrate de leer y seguir nuestras reglas para mantener una experiencia agradable para todos.

🔹 **Reglas Básicas:**
1. Sé respetuoso con los demás.
2. No compartas spoilers sin advertir.
3. Usa los canales adecuados para tus mensajes.

Para obtener más información, visita el canal de **#informacion**.

¡Que disfrutes tu estadía y buen juego!

**El equipo de Tarkov Server**
"""

# Evento cuando un nuevo miembro se une al servidor
@bot.event
async def on_member_join(member):
    # Canal de bienvenida, asegúrate de reemplazar 'welcome' con el nombre de tu canal
    welcome_channel = discord.utils.get(member.guild.text_channels, name='general')

    if welcome_channel:
        embed = discord.Embed(title="¡Bienvenido a **Escape from Tarkov**!", description=WELCOME_MESSAGE, color=0x00ff00)
        embed.set_thumbnail(url='https://ibb.co/rxk4xVS')  # Asegúrate de usar la URL directa a la imagen
        await welcome_channel.send(embed=embed)
        
# Define el árbol de comandos para los comandos de barra
@bot.event
async def on_ready():
    print(f'Nos hemos conectado como {bot.user}')
    print(f'Comandos disponibles: {", ".join([c.name for c in bot.commands])}')
    
    # Sincroniza los comandos de barra con Discord
    await bot.tree.sync()

@tree.command(name="weapon", description="Obtén información sobre una arma específica")
async def weapon(interaction: discord.Interaction, weapon_name: str):
    weapon_info = buscar_arma(weapon_name)  # Buscar el arma en el archivo JSON

    if weapon_info:
        # Verificar que la clave 'name' exista
        weapon_name = weapon_info.get('name', 'Nombre no disponible')
        weapon_description = weapon_info.get('description', 'Descripción no disponible')
        weapon_damage = weapon_info.get('damage', 'No disponible')
        weapon_fire_rate = weapon_info.get('fire_rate', 'No disponible')

        # Crear el embed
        embed = discord.Embed(title=weapon_name, description=weapon_description, color=0x00ff00)
        embed.add_field(name="Daño", value=weapon_damage, inline=False)
        embed.add_field(name="Cadencia de fuego", value=weapon_fire_rate, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"No se encontró información para el arma '{weapon_name}'.")

@tree.command(name="map", description="Obtén información sobre un mapa específico")
async def map(interaction: Interaction, map_name: str):
    # Aquí debes reemplazar 'data' con la fuente real de tus datos
    map_name = map_name.lower()
    map_info = data['maps'].get(map_name, data)  # Asegúrate de definir 'data'
    
    if map_info:
        embed = discord.Embed(title=map_info['name'], description=map_info['description'], color=0x00ff00)
        embed.add_field(name="Key Points", value='\n'.join(map_info['key_points']))
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('Mapa no encontrado. Por favor, proporciona un nombre de mapa válido.')
        
@tree.command(name="ammo", description="Obtén información sobre un tipo de munición")
async def municion(interaction: Interaction, ammo_name: str):
    ammo_name = ammo_name.lower()
    ammo = data['ammunition'].get(ammo_name, None)
    
    if ammo:
        embed = discord.Embed(title=ammo['name'], description=ammo['description'], color=0x00ff00)
        embed.add_field(name="Damage", value=ammo['damage'])
        embed.add_field(name="Penetration", value=ammo['penetration'])
        embed.add_field(name="Armor Class", value=ammo['armor_class'])
        embed.add_field(name="Recoil", value=ammo['recoil'])
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Munición no encontrada.")
        
@tree.command(name="jefe", description="Obtén información sobre un jefe específico")
async def jefe(interaction: discord.Interaction, boss_name: str):
    # Buscar el jefe en los datos
    boss = next((boss for boss in bosses_data if boss['name'].lower() == boss_name.lower()), None)

    # Si no se encuentra el jefe, mandar mensaje de error
    if not boss:
        await interaction.response.send_message(f"No se encontró información para el jefe '{boss_name}'.", ephemeral=True)
        return

    # Crear el embed con la información del jefe
    embed = discord.Embed(title=boss['name'], description=boss['description'], color=0x00ff00)
    embed.add_field(name="Ubicación", value=boss['location'], inline=False)
    embed.add_field(name="Debilidad", value=boss['weakness'], inline=False)
    embed.add_field(name="Objetos que deja", value=", ".join(boss['drops']), inline=False)

    # Enviar el embed como respuesta a la interacción
    await interaction.response.send_message(embed=embed)



# Comando de ayuda
@tree.command(name="help", description="Lista todos los comandos disponibles y su descripción")
async def help(interaction: discord.Interaction):
    # Crear el embed con estilo visual
    embed = discord.Embed(
        title="🔍 Comandos de ayuda de Tarkov Bot",
        description="Aquí tienes la lista de comandos disponibles para interactuar con el bot.",
        color=0x1abc9c  # Color verde azulado
    )
    
    # Información general del bot
    embed.set_thumbnail(url="https://link-al-banner-tarkov.com/banner.jpg")  # Cambia por una imagen relevante
    embed.set_footer(text="Tarkov Bot • Los mejores recursos para tu experiencia en Escape From Tarkov", icon_url="https://link-al-icono-footer.com/icon.png")
    
    # Agregar comandos con descripción
    embed.add_field(
        name="⚙️ `/ammo <nombre>`",
        value="Consulta la información detallada de una munición específica.",
        inline=False
    )
    embed.add_field(
        name="🔫 `/weapon <nombre>`",
        value="Obtén información sobre cualquier arma disponible en Escape From Tarkov.",
        inline=False
    )
    embed.add_field(
        name="💰 `/market <item>`",
        value="Muestra los precios actuales del mercado para un objeto.",
        inline=False
    )
    embed.add_field(
        name="🎯 `/boss <nombre>`",
        value="Te da detalles de los jefes en Escape From Tarkov (ubicaciones, habilidades, etc.).",
        inline=False
    )
    embed.add_field(
        name="🛠️ `/help`",
        value="Muestra este menú de ayuda con todos los comandos disponibles.",
        inline=False
    )

    # Estética adicional (imagen decorativa)
    embed.set_image(url="https://link-a-banner-inferior.com/banner_tarkov.png")  # Cambia por una imagen decorativa o del juego
    
    # Enviar el embed
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
