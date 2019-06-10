import discord

from .base import RoleShopBase


class RoleShopPoints(RoleShopBase):

    @RoleShopBase.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        profile = await self.bot.profile_cache.get_guild_profile(message.author.id, message.guild.id)
        if profile and not profile.in_points_buffer:
            self.bot.loop.create_task(profile.give_default_points())

    @RoleShopBase.group(invoke_without_command=True)
    async def points(self, ctx, *, member: discord.Member = None):
        if member:
            adverb = f"{member.name} has"
        else:
            member = ctx.author
            adverb = f"{member.name}, you have"
        if member.bot:
            return await ctx.send_line("🤖    Robos don't earn points.")

        profile = await self.bot.profile_cache.get_guild_profile(member.id, ctx.guild.id)
        await ctx.send_line(f"💰    {adverb} {profile.points} guild points.")

    @points.command(name="daily")
    async def daily_points(self, ctx, *, member: discord.Member = None):
        author_profile = await self.bot.profile_cache.get_guild_profile(ctx.author.id, ctx.guild.id)
        target_name = "you"
        if (member and member.bot) or not member:
            target_profile = author_profile
        else:
            target_profile = await self.bot.profile_cache.get_guild_profile(member.id, ctx.guild.id)
            if target_profile is None:
                target_profile = author_profile
            else:
                target_name = member.display_name
        if not author_profile.can_take_daily_points:
            res = f"⏳    You can redeem daily points again in {author_profile.next_daily_points.humanize()}."
            return await ctx.send_line(res)

        daily_points = await author_profile.take_daily_points(target_profile)
        res = f"🗓    {daily_points} daily points were given to {target_name}."
        await ctx.send_line(res)

    @points.command(name="credit", aliases=["transfer", "give"])
    async def transfer_points(self, ctx, points: int, *, member: discord.Member):
        if member.bot:
            return await ctx.send_line("❌    You can't transfer points to robos.")
        if points < 0:
            return await ctx.send_line("❌    Sorry but I suck at calculations involving negative numbers.")
        author_profile = await self.bot.profile_cache.get_guild_profile(ctx.author.id, ctx.guild.id)
        target_profile = await self.bot.profile_cache.get_guild_profile(member.id, ctx.guild.id)
        if author_profile.points < points:
            return await ctx.send_line("❌    Sorry but you don't have enough points to complete this transaction.")
        author_profile.give_points(-points)
        target_profile.give_points(points)
        await ctx.send_line(f"📤    {ctx.author.name}, you gave {points} points to {member.display_name}.")
