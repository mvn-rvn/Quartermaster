import discord
from discord.ext import commands
import aiosqlite


class ServListUpd(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()

        await cursor.execute("SELECT ServerID FROM ServerConfigs")
        old_guild_id_list: list[int] = [i[0] for i in await cursor.fetchall()]
        new_guild_id_list: list[int] = [i.id for i in self.bot.guilds]

        for new_guild_id in new_guild_id_list:
            if new_guild_id not in old_guild_id_list:

                await cursor.execute(f"""
                    INSERT INTO ServerConfigs (
                        ServerID,
                        StealChance,
                        StealCooldown,
                        FindEnabled
                    ) VALUES (
                        {new_guild_id},
                        0,
                        0,
                        1
                    )
                """)

        await db.commit()
        await cursor.close()
        await db.close()
    

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        db = await aiosqlite.connect("inv_manager.db")
        cursor = await db.cursor()

        await cursor.execute("SELECT ServerID FROM ServerConfigs")
        guild_id_list: list[int] = [i[0] for i in await cursor.fetchall()]

        if guild.id not in guild_id_list:
            await cursor.execute(f"""
                INSERT INTO ServerConfigs (
                    ServerID,
                    StealChance,
                    StealCooldown,
                    FindEnabled
                ) VALUES (
                    {new_guild_id},
                    0,
                    0,
                    1
                )
            """)

        await db.commit()
        await cursor.close()
        await db.close()


def setup(bot):
    bot.add_cog(ServListUpd(bot))