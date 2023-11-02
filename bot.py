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

# Load configurations
configurations = config.get("configs")

if configurations is not None:
    configs_list = [dict({
        "name": configuration.get("name", ""),
        "enabled": configuration.get("enabled", False),
        "keywords": configuration.get("keywords", []),
        "image_name": configuration.get("image_name", "")
        "custom_message": configuration.get("custom_message", "")
    }) for configuration in configurations]

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

    for config_instance in configs_list:
        if config_instance["enabled"]:
            re_lst = r"\b(?:{})\b".format("|".join(config_instance["keywords"]))
            match_word = re.search(re_lst, message_content.lower())

            if match_word and (not on_cooldown(message.author.id))
                with open("./assets/" + config_instance["image_name"], 'rb') as image_file:
                        image = discord.File(image_file)
                        await message.reply(config_instance["custom_message"], file=image)
                        return
            elif match_word and flood_msg_check():
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
    await ctx.respond("PAI BOT\n\n*Comandos*\n1- paibot docs: Documentação Oficial do papai'")

# Start the bot
bot.run(TOKEN)
