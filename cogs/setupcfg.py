import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import aiosqlite
import sqlite3

from permshandling import permshandler
from commonerrmsgs import errmsgs


class SetupCfg(commands.Cog):


    def __init__(self, bot: discord.Bot):
        self.bot = bot


    setup = SlashCommandGroup("setup", "(RESTRICTED) Configure role-based privileges and enable/disable certain commands")


    @setup.command(description = "(RESTRICTED) Set which role is able to use restricted commands")
    async def restricted_access(self, ctx: discord.ApplicationContext, role: discord.Role):

        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(await errmsgs.no_perms_embed(ctx))

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        await cursor.execute(f"""
            UPDATE ServerConfigs
            SET RoleID = {role.id}
            WHERE ServerID = {ctx.guild.id}
        """)

        await db.commit()
        await cursor.close()
        await db.close()

        await ctx.respond("yo we updated the shit and stuff")

        


def setup(bot):
    bot.add_cog(SetupCfg(bot))