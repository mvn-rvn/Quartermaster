import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import aiosqlite

from permshandling import permshandler
from commonerrmsgs import errmsgs

#includes give, transfer, remove, inventory, peek
class BasicInvManip(commands.Cog):