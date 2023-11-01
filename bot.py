import os
import discord
from discord.ext import commands
from PIL import Image
import time
import numpy as np
from dotenv import load_dotenv
import json
import sys
import re

load_dotenv()

cooldowns = {}
adm_id = int(os.environ["ADM_ID"])
mod_id = []

if os.path.exists('pai_config.json'):
    with open('pai_config.json', 'r') as config_file:
        config = json.load(config_file)
else:
    print('Error: config file not found')
    sys.exit(1)

# Load cooldown configuration
COOLDOWN = config.get("cooldown", 120)

# Load Nubank configuration
nubank_config = config.get("nubank_config", {})
nubank_enabled = nubank_config.get("enabled", False)
nubank_keywords = nubank_config.get("keywords", [])
nubank_image_name = nubank_config.get("image_name", "")

# Load Inter configuration
inter_config = config.get("inter_config", {})
inter_enabled = inter_config.get("enabled", False)
inter_keywords = inter_config.get("keywords", [])
inter_image_name = inter_config.get("image_name", "")

# Load Java configuration
java_config = config.get("java_config", {})
java_enabled = java_config.get("enabled", False)
java_keywords = java_config.get("keywords", [])
java_image_name = java_config.get("image_name", "")

# Load Rust configuration
rust_config = config.get("rust_config", {})
rust_enabled = rust_config.get("enabled", False)
rust_keywords = rust_config.get("keywords", [])
rust_gif_address = rust_config.get("gif_address", "")

def on_cooldown(id):
    if id == adm_id:
        return False
    elif id not in cooldowns or (time.time() - cooldowns[id]) > COOLDOWN:
        # Update the last triggered time
        cooldowns[id] = time.time()
        return False
    else:
        return True

def flood_msg_check():
    choice = np.random.randint(1, 11)
    if choice == 1:
        return True
    else:
        return False

# INTENTS
intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.message_content = True

# BOT TOKEN
TOKEN = os.environ["TOKEN"]

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# ready log
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Event handler for when a message is received
@bot.event
async def on_message(message):
    print(adm_id == message.author.id) # debug
    # Ignore messages from the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # adm functions - REFACTORING NEEDED (Probably better w/ slash commands)
    if message.author.id == adm_id:
        if "modpai" in message.content.lower():
            if "add" in message.content.lower():
                id = message.content[-18:]
                if id not in mod_id:
                    mod_id.append(id)
                    await message.reply(f'<@{id}> agora é um mod do papai')
                else:
                    await message.reply('ele já é mod seu zé ruela')
            elif "remove" in message.content.lower():
                id = message.content[-18:]
                if id not in mod_id:
                    await message.reply('ele já não era meu mod')
                else:
                    mod_id.remove(id)
                    await message.reply(f'<@{id}> não é mais mod do papai')
        elif "pai xp" in message.content.lower():
            await message.reply('+xp')

    if nubank_enabled:
        for keyword in nubank_keywords:
            if re.search(r'\b' + keyword + r'\b', message.content.lower()) and (not on_cooldown(message.author.id)):
                # Send an image in response
                image_path = os.environ['img_path'] + nubank_image_name
                with open(image_path, 'rb') as image_file:
                    image = discord.File(image_file)
                    await message.reply('pow, filhão', file=image)
                return
            elif keyword in message.content.lower() and flood_msg_check():
                await message.reply('para de floodar seu desgraçado')

    if inter_enabled:
        for keyword in inter_keywords:
            if re.search(r'\b' + keyword + r'\b', message.content.lower()) and (not on_cooldown(message.author.id)):
                # Send an image in response
                image_path = os.environ['img_path'] + inter_image_name
                with open(image_path, 'rb') as image_file:
                    image = discord.File(image_file)
                    await message.reply('pow, filhão', file=image)
                return
            elif keyword in message.content.lower() and flood_msg_check():
                await message.reply('para de floodar seu desgraçado')

    if java_enabled:
        for keyword in java_keywords:
            if re.search(r'\b' + keyword + r'\b', message.content.lower()) and (not on_cooldown(message.author.id)):
                # Send an image in response
                image_path = os.environ['img_path'] + java_image_name
                with open(image_path, 'rb') as image_file:
                    image = discord.File(image_file)
                    await message.reply('pow, filhão', file=image)
                return
            elif keyword in message.content.lower() and flood_msg_check():
                await message.reply('para de floodar seu desgraçado')

    if rust_enabled:
        for keyword in rust_keywords:
            if re.search(r'\b' + keyword + r'\b', message.content.lower()) and (not on_cooldown(message.author.id)):
                # Send an gif in response
                await message.reply(rust_gif_address)
                return
            elif keyword in message.content.lower() and flood_msg_check():
                await message.reply('para de floodar seu desgraçado')

    # check for mention
    if bot.user.mentioned_in(message) and (not on_cooldown(message.author.id)):
        choose = np.random.randint(1, 4)
        if choose == 1:
            await message.reply('marca teu cu seu arrombado')
        elif choose == 2:
            await message.reply('*fui comprar cigarro, deixe seu recado*')
        elif choose == 3:
            await message.reply('pede pra tua mãe, to jogando truco')
    elif bot.user.mentioned_in(message) and flood_msg_check():
        await message.reply('para de floodar seu desgraçado')

    await bot.process_commands(message)

@bot.slash_command(
    name="paidocs",
    description="documentação do pai"
)
async def paidocs(ctx):
    await ctx.send("PAI BOT\n\n*Comandos*\n1- paibot docs: Documentação Oficial do papai'")

# Start the bot
bot.run(TOKEN)
