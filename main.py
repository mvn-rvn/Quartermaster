#built-in module imports
import os
import sqlite3


#external package imports
import discord
from discord.ext import commands
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
    StealLimit int,
    FindEnabled int
)""")

db_not_async.execute("""CREATE TABLE IF NOT EXISTS MasterInv (
    ItemLower text,
    ItemExact text,
    ServerID int,
    UserID int,
    MessageID int,
    Quantity int,
    Secret int
)""")

db_not_async.close()


@bot.slash_command(description="Test the bot's response time to Discord")
async def ping(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title = "Pong!",
        description = f"Latency is {round(bot.latency * 1000)}ms."
    )
    await ctx.respond(embed=embed)


#this is probably stupid ngl
@bot.check
def guilds_only(ctx: discord.ApplicationContext):
    if ctx.guild == None and ctx.command.cog.__cog_name__ != "Help":
        raise commands.NoPrivateMessage()
    return True

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            title = "Error",
            description = "This command can only be run in a server.",
            color = discord.Color.red()
        )
        await ctx.respond(embed=embed)


bot.load_extension('cogs.setupcfg')
bot.load_extension('cogs.servlistupd')
bot.load_extension('cogs.basicinvmanip')


#bot run
bot.run(TOKEN)
