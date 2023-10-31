import os
import discord
from discord.ext import commands
from PIL import Image
import time
import numpy as np
from dotenv import load_dotenv

load_dotenv()

COOLDOWN = 60
cooldowns = {}
adm_id = int(os.environ["ADM_ID"])
mod_id = []

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

    # Check if the message contains a nubank-related word
    messages = ['clojure', 'nubank', 'roxinho', 'nu bank', 'nubenqui', 'nub ank', 'nuba nk', 'nuba', 'cloj', 'pelado bank', 'n u b a n k', 'c l o j u r e', 'n.u.b.a.n.k', 'c.l.o.j.u.r.e', 'n_u_b', 'c_l_o', 'naked b', 'nu_']
    for msg in messages:
        if (msg in message.content.lower()) and (not on_cooldown(message.author.id)):
            # Send an image in response
            image_path = os.environ['img_path'] + 'Nubank.jpg'
            with open(image_path, 'rb') as image_file:
                image = discord.File(image_file)
                await message.reply('pow, filhão', file=image)
            break
        elif msg in message.content.lower() and flood_msg_check():
            await message.reply('para de floodar seu desgraçado')
            break

    # check for inter
    if 'inter ' in message.content.lower() and (not on_cooldown(message.author.id)):
        image_path = os.environ['IMG_PATH'] + 'inter.png'
        print(image_path)
        with open(image_path, 'rb') as image_file:
            image = discord.File(image_file)
            await message.reply('pow, filhão', file=image)
    elif 'inter ' in message.content.lower() and flood_msg_check():
        await message.reply('para de floodar seu desgraçado')

    # check for rust
    if 'rust' in message.content.lower() and (not on_cooldown(message.author.id)):
        await message.reply('https://tenor.com/view/rust-femboy-rust-femboy-programming-rust-programming-gif-27321790')
    elif 'rust' in message.content.lower() and flood_msg_check():
        await message.reply('para de floodar seu desgraçado')

    # check for java
    if ((message.content.lower() == 'java') or ('java ' in message.content.lower())) and (not on_cooldown(message.author.id)):
        image_path = os.environ['img_path'] + 'java.png'
        with open(image_path, 'rb') as image_file:
            image = discord.File(image_file)
            await message.reply('java kkkkkk', file=image)
    elif 'java' in message.content.lower() and flood_msg_check():
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
