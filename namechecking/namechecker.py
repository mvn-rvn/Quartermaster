import discord
import aiosqlite


async def check_exists_caseins(ctx: discord.ApplicationContext, input_name: str) -> tuple[bool, str]:
    
    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    
    await cursor.execute("""
        SELECT ItemExact
        FROM MasterInv
        WHERE ServerID = ? AND ItemLower = ?
    """, (ctx.guild.id, input_name.lower()))

    db_name: str = await cursor.fetchone()[0]
    
    await cursor.close()
    await db.close()
    
    if db_name == None:
        return (False, input_name)
    else:
        return (True, db_name)


async def check_secret_name_conflict(ctx: discord.ApplicationContext, input_name: str, input_secret: bool) -> bool:

    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    
    await cursor.execute("""
        SELECT ItemExact, Secret
        FROM MasterInv
        WHERE ServerID = ? AND ItemLower = ?
    """, (ctx.guild.id, input_name.lower()))
    
    data: tuple[str, int] = await cursor.fetchone()
    
    if data == None:
        await cursor.close()
        await db.close()
        return False
    
    await cursor.close()
    await db.close()
    
    db_secret: bool = False
    if data[1] == 1:
        db_secret = True

    return input_secret == db_secret