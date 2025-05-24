# OS
import sys
import os

# MongoDB
from pymongo import database
import requests

# Discord
import discord
import aiohttp
from discord import Webhook, app_commands
from discord.ext import commands
from discord import Interaction
import pymongo
from pymongo.mongo_client import MongoClient

# Token
import Tokens

# Modules
from Modules.BotCommands.bot_commands import BotCommands


m_file = open("/Tokens/mongodb_token.txt")
mongo_url = m_file.read()

try:    
    print("Initializing MongoDB client...")
    mClient = MongoClient(mongo_url)
except Exception as e:
    print(e)
    
d_file = open("/Tokens/discord_token.txt")
token = d_file.read()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


@bot.tree.context_menu(name="Information") #, guild=guildID
async def info(interaction : discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", description=f"ID: {member.id}")
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles]), inline=False)
    embed.add_field(name="Badges", value=", ".join([badge.name for badge in member.public_flags.all()]), inline=False)
    embed.add_field(name="Activity", value=member.activity)
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.activity.Game("Loading"))

    #Connect to mongoDB
    try:
        local = mClient.list_databases()
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return

    #Add cogs
    await bot.add_cog(BotCommands(bot, mClient=mClient))

    #Sync command tree
    await bot.tree.sync()

    # Update presence
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("Linking")
    )

    print("Ready!")
    
bot.run(token)