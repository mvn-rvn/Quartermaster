import discord
import aiosqlite


class ItemData:
    
    def __init__(self, exists: bool, name: str, quantity: int, secret: bool):
        self.exists = exists
        self.name = name
        self.quantity = quantity
        self.secret = secret
        
    def __str__(self):
        return f"""EXISTS: {self.exists}
            NAME: {self.name}
            QUANTITY: {self.quantity}
            SECRET: {self.secret}"""


async def check_exists(ctx: discord.ApplicationContext, input_name: str, user_id: int = None) -> ItemData:
    
    db = await aiosqlite.connect("inv_manager.db")
    cursor = await db.cursor()
    
    if user_id != None:
        await cursor.execute("""
            SELECT ItemExact, Quantity, Secret
            FROM MasterInv
            WHERE ServerID = ? 
            AND ItemLower = ?
            AND UserID = ?
        """, (ctx.guild.id, input_name.lower(), user_id))
    
    else:
        await cursor.execute("""
            SELECT ItemExact, Quantity, Secret
            FROM MasterInv
            WHERE ServerID = ? 
            AND ItemLower = ?
        """, (ctx.guild.id, input_name.lower()))

    data = await cursor.fetchone()
    
    await cursor.close()
    await db.close()
    
    if data == None:
        return ItemData(False, None, None, None)
    
    db_name: str = data[0]
    db_quantity: int = data[1]
    
    db_secret: bool = False
    if data[2] == 1:
        db_secret = True
    
    return ItemData(True, db_name, db_quantity, db_secret)