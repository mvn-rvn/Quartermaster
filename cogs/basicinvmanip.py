import discord
from discord.ext import commands
import aiosqlite

from permshandling import permshandler
from commonerrmsgs import errmsgs
from namechecking import namechecker

#includes give, transfer, remove, inventory, peek
class BasicInvManip(commands.Cog):
    
    
    def __init__(self, bot: discord.Bot):
        self.bot = bot
