import discord
from discord.ext import commands
import aiosqlite

from permshandling import permshandler
from commonerrmsgs import errmsgs
from userinvchecking import invchecker
from userinvchecking.invchecker import ItemData

#includes give, transfer, remove, inventory, peek
class BasicInvManip(commands.Cog):
    
    
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    
    @commands.slash_command(description = "(RESTRICTED) Creates an item and puts it in a user's inventory")
    async def give(self, ctx: discord.ApplicationContext, user: discord.Member, name: str, quantity: int = 1, is_secret: bool = False):
        
        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await errmsgs.no_perms_embed(ctx))
            return
        
        if quantity < 1:
            await ctx.respond(embed = errmsgs.quantity_less_than_one())
            return
        
        db_data_global: ItemData = await invchecker.check_exists(ctx, name)
        
        if db_data_global.exists == True and db_data_global.secret != is_secret:
            await ctx.respond(embed = errmsgs.naming_conflict(is_secret))
            return
        
        if db_data_global.name != None:
            name = db_data_global.name
            
        is_secret_int: int = 0
        if is_secret == True:
            is_secret_int = 1
            
        db_data_user: ItemData = await invchecker.check_exists(ctx, name, user.id)
            
        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        if db_data_user.exists == True:
            await cursor.execute("""
                UPDATE MasterInv
                SET Quantity = Quantity + ?
                WHERE ItemLower = ?
                AND ServerID = ?
                AND UserID = ?
            """, (quantity, name.lower(), ctx.guild.id, user.id))
            
        else:
            await cursor.execute("""
                INSERT INTO MasterInv (
                    ItemLower,
                    ItemExact,
                    ServerID,
                    UserID,
                    Quantity,
                    Secret
                ) VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            """, (name.lower(), name, ctx.guild.id, user.id, quantity, is_secret_int))
        
        await db.commit()
        await cursor.close()
        await db.close()
        
        if is_secret == True:
            name = f"__{name}__"
        if quantity == 1:
            await ctx.respond(f"Gave {name} to <@{user.id}>.")
        else:
            await ctx.respond(f"Gave {quantity}x {name} to <@{user.id}>.")
        
        
        
        
        
        
def setup(bot):
    bot.add_cog(BasicInvManip(bot))