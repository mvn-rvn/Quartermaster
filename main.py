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

'''
#configure (role, steal_chance): creates server's associated JSON file if it doesn't exist, and sets admin role and steal chance in that file.
#steal_chance defaults to 0 if not specified
@bot.slash_command(name="setup", description="(RESTRICTED) Configure steal settings and what role has access to restricted commands")
@discord.ext.commands.guild_only()
async def setup(ctx: discord.ApplicationContext, role: discord.Role, steal_chance: int = 0, steal_cooldown: int = 24):
    #check if user has privileges to run the command
    if await check_perms(ctx) == False:
        #send embed saying user doesn't have privileges
        embed = discord.Embed(
            title = "Uh-oh",
            description = await no_perms_message(ctx),
            color = discord.Color.red()
        )
        await ctx.respond(embed=embed)
        #end function early
        return
    #check if steal_chance is between 0 and 100
    if steal_chance > 100 or steal_chance < 0:
        #send embed detailing error
        embed = discord.Embed(
            title = "Uh-oh", 
            description = "Steal chance must be between 0 and 100.",
            color = discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return
    #check if steal_cooldown is positive
    if steal_cooldown < 0:
        #send embed detailing error
        embed = discord.Embed(
            title = "Uh-oh", 
            description = "Steal cooldown must be a positive number.",
            color = discord.Color.red()
        )
        await ctx.respond(embed=embed)
        #end function early
        return
    #open database
    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    #check if server's associated row already exists
    await cursor.execute(f"SELECT ServerID FROM ServerConfigs")
    if await cursor.fetchone() == None:
        #creates row if it doesn't exist
        await cursor.execute(f"""INSERT INTO ServerConfigs (
            ServerID, 
            RoleID, 
            StealChance, 
            StealCooldown
        ) VALUES (
            {ctx.guild.id}, 
            {role.id}, 
            {steal_chance}, 
            {steal_cooldown}
        )""")
        #send embed saying server config has been created
        embed = discord.Embed(title = "Server configuration created!")
        embed.add_field(name = "Role", value = f"`@{role.name}`", inline = False)
        embed.add_field(name = "Steal Chance", value = f"{steal_chance}%", inline = False)
        embed.add_field(name = "Steal Cooldown", value = f"{steal_cooldown} hours", inline = False)
        await ctx.respond(embed = embed)
    else:
        #updates row if it already exists
        await cursor.execute(f"""UPDATE ServerConfigs 
        SET RoleID = {role.id}, StealChance = {steal_chance}, StealCooldown = {steal_cooldown} 
        WHERE ServerID = {ctx.guild.id}""")
        #send embed saying server config has been updated
        embed = discord.Embed(title = "Server configuration updated!")
        embed.add_field(name = "Role", value = f"`@{role.name}`", inline = False)
        embed.add_field(name = "Steal Chance", value = f"{steal_chance}%", inline = False)
        embed.add_field(name = "Steal Cooldown", value = f"{steal_cooldown} hours", inline = False)
        await ctx.respond(embed = embed)
    #commit and close database
    await db.commit()
    await cursor.close()
    await db.close()
'''

bot.load_extension('cogs.setupcfg')
bot.load_extension('cogs.servlistupd')

#bot run
bot.run(TOKEN)