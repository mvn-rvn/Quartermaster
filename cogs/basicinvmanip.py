import discord
from discord.ext import commands
import aiosqlite

from modules import permshandler
from modules import commonerrmsgs
from modules import invchecker
from modules.invchecker import ItemData

#includes give, transfer, remove, inventory, peek
class BasicInvManip(commands.Cog):
    
    
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    
    @commands.slash_command(description = "(RESTRICTED) Creates an item and puts it in a user's inventory")
    async def give(self, ctx: discord.ApplicationContext, user: discord.Member, name: str, quantity: int = 1, is_secret: bool = False):
        
        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await commonerrmsgs.no_perms_embed(ctx), ephemeral=True)
            return
        
        if quantity < 1:
            await ctx.respond(embed = commonerrmsgs.quantity_less_than_one(), ephemeral=True)
            return
        
        name_case_corrected: str
        
        db_data_global: ItemData = await invchecker.check_exists(ctx, name)
        
        if db_data_global == None:
            name_case_corrected = name
            
        elif db_data_global.secret != is_secret:
            await ctx.respond(embed = commonerrmsgs.naming_conflict(is_secret), ephemeral=True)
            return
        
        else:
            name_case_corrected = db_data_global.name
            
        db_data_user: ItemData = await invchecker.check_exists(ctx, name_case_corrected, user.id)
        
        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        if db_data_user == None:
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
            """, (name_case_corrected.lower(), name_case_corrected, ctx.guild.id, user.id, quantity, int(is_secret)))
        
        else:
            await cursor.execute("""
                UPDATE MasterInv
                SET Quantity = Quantity + ?
                WHERE ItemLower = ?
                AND ServerID = ?
                AND UserID = ?
            """, (quantity, name_case_corrected.lower(), ctx.guild.id, user.id))
        
        await db.commit()
        await cursor.close()
        await db.close()
        
        displayed_name: str
        
        if is_secret == True:
            displayed_name = f"__{name_case_corrected}__"
        else:
            displayed_name = name_case_corrected
        
        if quantity == 1:
            await ctx.respond(f"Gave {displayed_name} to <@{user.id}>.")
        else:
            await ctx.respond(f"Gave {quantity}x {displayed_name} to <@{user.id}>.")
            
      
    @commands.slash_command(description = "(RESTRICTED) Removes a specified item from a user's inventory")
    async def remove(self, ctx: discord.ApplicationContext, user: discord.Member, name: str, quantity: int = 1):
        
        if await permshandler.check_perms(ctx) == False:
            await ctx.respond(embed = await commonerrmsgs.no_perms_embed(ctx), ephemeral=True)
            return
        
        if quantity < 1:
            await ctx.respond(embed = commonerrmsgs.quantity_less_than_one(), ephemeral=True)
            return
        
        db_data_user: ItemData = await invchecker.check_exists(ctx, name, user.id)
        
        if db_data_user == None:
            await ctx.respond(embed = commonerrmsgs.item_doesnt_exist(username = user.name), ephemeral=True)
            return
        
        if db_data_user.quantity < quantity:
            await ctx.respond(embed = commonerrmsgs.quantity_too_high(user.name), ephemeral=True)
            return
        
        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()
        
        if db_data_user.quantity == quantity:
            await cursor.execute("""
                DELETE FROM MasterInv
                WHERE ItemLower = ?
                AND ServerID = ?
                AND UserID = ?
            """, (name.lower(), ctx.guild.id, user.id))
        
        else:
            await cursor.execute("""
                UPDATE MasterInv
                SET Quantity = Quantity - ?
                WHERE ItemLower = ?
                AND ServerID = ?
                AND UserID = ?
            """, (quantity, name.lower(), ctx.guild.id, user.id))
        
        await db.commit()
        await cursor.close()
        await db.close()
        
        name_case_corrected: str = db_data_user.name
        
        displayed_name: str
        
        if db_data_user.secret == True:
            displayed_name = f"__{name_case_corrected}__"
        else:
            displayed_name = name_case_corrected
        
        if quantity == 1:
            await ctx.respond(f"Removed {displayed_name} from <@{user.id}>'s inventory.")
        else:
            await ctx.respond(f"Removed {quantity}x {displayed_name} from <@{user.id}>'s inventory.")
        
        
        
        
        
        
        
        
def setup(bot):
    bot.add_cog(BasicInvManip(bot))