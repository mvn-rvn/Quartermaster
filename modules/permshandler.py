import discord
import aiosqlite


async def grab_restricted_role_id(ctx: discord.ApplicationContext) -> int:

    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()

    await cursor.execute("""
        SELECT RoleID 
        FROM ServerConfigs
        WHERE ServerID = ?
    """, (ctx.guild.id,))

    role_id: tuple[int] = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return role_id[0]


async def check_perms(ctx: discord.ApplicationContext) -> bool:
    
    role_id = await grab_restricted_role_id(ctx)

    for role in ctx.author.roles:
        if role.id == role_id:
            return True
    
    return ctx.channel.permissions_for(ctx.author).administrator