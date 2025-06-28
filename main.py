#built-in module imports
import os
import sqlite3


#external package imports
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


bot.load_extension('cogs.setupcfg')
bot.load_extension('cogs.servlistupd')
bot.load_extension('cogs.basicinvmanip')


#bot run
bot.run(TOKEN)