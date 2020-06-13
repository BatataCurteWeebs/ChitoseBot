import discord
from discord.ext import commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="nada"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} foi kickado por {ctx.author.mention} por {reason}.")
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def aniquilar(self, ctx, member: discord.Member, *, reason="Sem motivo"):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} foi ANIQUILADO por {ctx.author.mention} por {reason}. Não seja como ele.")
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def apagar(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} mensagens foram apagadas.")
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def aviso(self, ctx, member: discord.Member, *, reason="Sem motivo"):
        await ctx.send(f"{member.mention} foi ALERTADO por {ctx.author.mention} por {reason}.")

def setup(bot):
    bot.add_cog(mod(bot))
