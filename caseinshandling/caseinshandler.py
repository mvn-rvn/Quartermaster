import discord
import aiosqlite


async def case_ins_check(ctx: discord.ApplicationContext, name: str) -> str:
    
    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    
    await cursor.execute("""
        SELECT ItemExact
        FROM MasterInv
        WHERE ServerID = ? AND ItemLower = ?
    """, (ctx.guild.id, name.lower()))

    exact_name: tuple[str] = await cursor.fetchone()
    
    if exact_name == None:
        return name
    else:
        return exact_name[0]