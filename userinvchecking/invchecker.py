import discord
import aiosqlite


async def check_exists(ctx: discord.ApplicationContext, input_name: str) -> tuple[bool, str, int, bool]:
    
    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    
    await cursor.execute("""
        SELECT ItemExact, Quantity, Secret
        FROM MasterInv
        WHERE ServerID = ? AND ItemLower = ?
    """, (ctx.guild.id, input_name.lower()))

    data = await cursor.fetchone()
    
    await cursor.close()
    await db.close()
    
    if data == None:
        return (False, None, None, None)
    
    db_name: str = data[0]
    db_quantity: int = data[1]
    
    db_secret: bool = False
    if data[2] == 1:
        db_secret = True
    
    return (True, db_name, db_quantity, db_secret)
