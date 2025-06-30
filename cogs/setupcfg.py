import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import aiosqlite

from permshandling import permshandler
from commonerrmsgs import errmsgs


class SetupCfg(commands.Cog):


    def __init__(self, bot: discord.Bot):
        self.bot = bot


    setupcfg = SlashCommandGroup("setup", "(RESTRICTED) Configure role-based privileges and tweak certain commands")


    @setupcfg.command(description = "(RESTRICTED) Set which role is able to use restricted commands")
    async def restricted_access(self, ctx: discord.ApplicationContext, role: discord.Role):

        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await errmsgs.no_perms_embed(ctx))
            return

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        await cursor.execute("""
            UPDATE ServerConfigs
            SET RoleID = ?
            WHERE ServerID = ?
        """, (role.id, ctx.guild.id))

        await db.commit()
        await cursor.close()
        await db.close()

        embed = discord.Embed(
            title = "Restricted access updated",
            description = f"Role <@&{role.id}> has access to restricted commands.",
            color = discord.Color.green()
        )

        await ctx.respond(embed=embed)


    @setupcfg.command(description = "(RESTRICTED) Configure settings for the /steal command")
    async def stealing(self, ctx: discord.ApplicationContext, success_rate: int, cooldown: int, quantity_limit: int):

        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await errmsgs.no_perms_embed(ctx))
            return

        if success_rate > 100 or success_rate < 0:
            embed = discord.Embed(
                title = "Error",
                description = "Success rate cannot be less than 0 or greater than 100.",
                color = discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if cooldown < 0:
            embed = discord.Embed(
                title = "Error",
                description = "Cooldown cannot be less than 0.",
                color = discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return
        
        if quantity_limit < 1:
            await ctx.respond(embed = errmsgs.quantity_less_than_one())
            return

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()

        await cursor.execute("""
            UPDATE ServerConfigs
            SET StealChance = ?, 
                StealCooldown = ?,
                StealLimit = ?
            WHERE ServerID = ?
        """, (success_rate, cooldown, quantity_limit, ctx.guild.id))

        await db.commit()
        await cursor.close()
        await db.close()

        embed = discord.Embed(
            title = "Steal command configurations updated",
            color = discord.Color.green()
        )

        embed.add_field(name = "Steal Command Success Rate", value = f"{success_rate}%", inline = False)
        if cooldown == 1:
            embed.add_field(name = "Steal Command Cooldown", value = f"{cooldown} hour", inline = False)
        else:
            embed.add_field(name = "Steal Command Cooldown", value = f"{cooldown} hours", inline = False)
        embed.add_field(name = "Steal Quantity Limit", value = f"{quantity_limit}", inline = False)

        await ctx.respond(embed=embed)
    

    @setupcfg.command(description = "(RESTRICTED) Enable or disable the /find command")
    async def finding(self, ctx: discord.ApplicationContext, enabled: bool):

        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await errmsgs.no_perms_embed(ctx))
            return

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        enabled_int: int = 0

        if enabled == True:
            enabled_int = 1
            embed = discord.Embed(
                title="Find command enabled.",
                color = discord.Color.green()
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Find command disabled.",
                color = discord.Color.green()
            )
            await ctx.respond(embed=embed)

        await cursor.execute("""
            UPDATE ServerConfigs
            SET FindEnabled = ?
            WHERE ServerID = ?
        """, (enabled_int, ctx.guild.id))

        await db.commit()
        await cursor.close()
        await db.close()


    @setupcfg.command(description = "View current configuration settings")
    async def view(self, ctx: discord.ApplicationContext):

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()

        await cursor.execute("""
            SELECT RoleID, StealChance, StealCooldown, StealLimit, FindEnabled
            FROM ServerConfigs
            WHERE ServerID = ?
        """, (ctx.guild.id,))
        
        configs = await cursor.fetchone()
        
        await cursor.close()
        await db.close()
        
        role: discord.Role = ctx.guild.get_role(configs[0])
        steal_success_rate: int = configs[1]
        steal_cooldown: int = configs[2]
        steal_quantity_limit = configs[3]
        
        embed = discord.Embed(
            title = f"{ctx.guild.name}'s Settings"
        )
        
        if role == None:
            embed.add_field(name = "Role-based Restricted Access", value = "N/A", inline = False)
        else:
            embed.add_field(name = "Role-based Restricted Access", value = f"<@&{role.id}>", inline = False)
        
        embed.add_field(name = "Steal Command Success Rate", value = f"{steal_success_rate}%", inline = False)
        
        if steal_cooldown == 1:
            embed.add_field(name = "Steal Command Cooldown", value = f"{steal_cooldown} hour", inline = False)
        else:
            embed.add_field(name = "Steal Command Cooldown", value = f"{steal_cooldown} hours", inline = False)
        
        embed.add_field(name = "Steal Quantity Limit", value = f"{steal_quantity_limit}", inline = False)
        
        if configs[4] == 1:
            embed.add_field(name = "Find Command", value = "Enabled", inline = False)
        else:
            embed.add_field(name = "Find Command", value = "Disabled", inline = False)
            
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(SetupCfg(bot))