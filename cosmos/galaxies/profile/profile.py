import discord

from .. import Cog
from .models import ProfileCache

from discord.ext import commands


class Profile(Cog):

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.cache = ProfileCache(self.plugin)
        if self.plugin.data.profile.__dict__.get("cache_all"):
            self.bot.loop.create_task(self.cache.prepare())

    def __is_ignored(self, message):
        if message.author.id == self.bot.user.id:
            return True
        if message.author.bot:
            return True
        if not message.guild:
            return True

    async def on_message(self, message):
        if self.__is_ignored(message):
            return

        await self.cache.give_xp(message)

    @commands.command()
    async def profile(self, ctx, user: discord.User = None):
        user = user or ctx.author
        profile = await self.cache.get_profile(user.id)
        await ctx.send(embed=profile.get_embed())

    @commands.command(name="rep")
    async def rep_user(self, ctx, user: discord.User):
        author_profile = await self.cache.get_profile(ctx.author.id)
        if author_profile.can_rep:
            target_profile = await self.cache.get_profile(user.id)
            if not target_profile:
                res = f"Sorry but, {user.name} hasn't created their Cosmos Profile yet."
                embed = self.bot.theme.embeds.one_line.primary(res)
                await ctx.send(embed=embed)
            target_profile.rep()
            embed = self.bot.theme.embeds.one_line.primary(f"👌 You added one reputation point to {user.name}.")
            await ctx.send(embed=embed)
        else:
            embed = self.bot.theme.embeds.one_line.primary(f"🕐 You can rep again in {author_profile.rep_delta}.")
            await ctx.send(embed=embed)
