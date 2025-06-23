import discord
import aiosqlite

from permshandling import permshandler


async def no_perms_text(ctx: discord.ApplicationContext) -> str:

    description: str

    role: discord.Role = ctx.guild.get_role(await permshandler.grab_restricted_role_id(ctx))

    if role == None:
        description = "Only users with Administrator privileges can use this command."
    else:
        description = f"Only users with Administrator privileges or the `@{role.name}` role can use this command."

    return description


async def no_perms_embed(ctx: discord.ApplicationContext) -> discord.Embed:

    description: str

    role: discord.Role = ctx.guild.get_role(await permshandler.grab_restricted_role_id(ctx))

    if role == None:
        description = "Only users with Administrator privileges can use this command."
    else:
        description = f"Only users with Administrator privileges or the `@{role.name}` role can use this command."

    embed = discord.Embed(
        title = "Error",
        description = description,
        color = discord.Color.red()
    )

    return embed


def quantity_less_than_one() -> discord.Embed:

    embed = discord.Embed(
        title = "Error",
        description = "Quantity cannot be less than one.",
        color = discord.Color.red()
    )

    return embed