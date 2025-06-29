import discord

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


def naming_conflict(variant: bool) -> discord.Embed:
    
    description: str
    
    if variant == True:
        description = "To avoid confusing the bot, a secret item cannot have the same name as a normal item."
    else:
        description = "To avoid confusing the bot, a normal item cannot have the same name as a secret item."
    
    embed = discord.Embed(
        title = "Error",
        description = description,
        color = discord.Color.red()
    )
    
    return embed


def quantity_too_high(username: str = None) -> discord.Embed:
    
    description: str
    
    if username == None:
        description = "Quantity is too high - you don't have enough of that item."
    else:
        description = f"Quantity is too high - {username} doesn't have enough of that item."
    
    embed = discord.Embed(
        title = "Error",
        description = description,
        color = discord.Color.red()
    )
    
    return embed


def item_doesnt_exist(username: str = None, self_inv: bool = False) -> discord.Embed:
    
    description: str
    
    if self_inv == True:
        description = "That item doesn't exist in your inventory!"
    elif username != None:
        description = f"That item doesn't exist in {username}'s inventory!" 
    else:
        description = "That item doesn't exist on this server!"
    
    embed = discord.Embed(
        title = "Error",
        description = description,
        color = discord.Color.red()
    )
    
    return embed