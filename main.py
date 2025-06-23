#built-in module imports
import os
import sqlite3
import json
import asyncio


#external package imports
import aiosqlite
import discord
import dotenv


#dotenv and bot setup
dotenv.load_dotenv()
TOKEN = str(os.getenv("TOKEN"))

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} online.")


#database setup
db_not_async = sqlite3.connect("inv_manager.db")
db_not_async.execute("""CREATE TABLE IF NOT EXISTS ServerConfigs (
    ServerID int PRIMARY KEY, 
    RoleID int, 
    StealChance int, 
    StealCooldown int,
    FindEnabled int
)""")
db_not_async.close()


#delete this later, I'm using it as an example of command structure
@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}! {ctx.channel.permissions_for(ctx.author).administrator}")


bot.load_extension('cogs.setupcfg')
bot.load_extension('cogs.servlistupd')

#bot run
bot.run(TOKEN)