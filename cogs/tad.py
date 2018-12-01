import discord
from discord.ext import commands
import datetime
from cogs.utils.util import get_reaction_yes_no, get_random_embed_color
from cogs.utils import checks

class TAD(object):
    """A custom class for tad server."""

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.invites = []
        self.bot.loop.create_task(self.get_guild_data())
        # self.rules = self.bot.get_channel(452702379293540372)
        # self.server_guide = self.bot.get_channel(269610314578788363)



        # bot.loop.create_task(self.rotate())

    async def get_guild_data(self):
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(244998983112458240)
        await self.get_invites()

    async def get_invites(self):
        self.invites = await self.guild.invites()

    '''async def rotate(self):
        await self.bot.wait_until_ready()
        m_rules = await self.rules.get_message(452756009811968001)
        m_punishments = await self.rules.get_message(452756043114479629)
        m_banner = await self.server_guide.get_message(452822879067832320)
        m_info = await self.server_guide.get_message(452822935049338881)'''

    async def __local_check(self, ctx):
        return ctx.guild.id in [244998983112458240]

    async def on_message(self, message):

        """if message.author.id == 280883146872979456 and message.attachments != []:
            await message.delete()
            await message.channel.send("lol steve fuck off")"""

    async def on_member_join(self, member):
        if member.guild.id == 244998983112458240:
            invite = None
            invites = await self.guild.invites()
            for i in invites:
                for old_invite in self.invites:
                    if i.uses > old_invite.uses and i.id == old_invite.id:
                        invite = i
            if not invite:
                async for entry in member.guild.audit_logs():
                    if entry.action == discord.AuditLogAction.invite_create:
                        invite = entry.target
                        break

            await self.get_invites()

            embed = discord.Embed(title="Member Joined", color=get_random_embed_color(), timestamp=member.joined_at)
            embed.add_field(name="Member", value=f"{member.mention} | {member}\n**ID:** `{member.id}`")
            embed.add_field(name="Joined at", value=f"{member.joined_at.strftime('%d - %B - %Y | %H : %M (GMT)')}")
            embed.add_field(name="Created at", value=f"{member.created_at.strftime('%d - %B - %Y')}")
            if invite is not None:
                if invite.created_at is not None:
                    embed.add_field(name="Invite", value=f"**URL:** {invite.url}\n**Inviter:** {invite.inviter.mention} | {invite.inviter}\n**Uses:** {invite.uses}\n**Created:** {invite.created_at.strftime('%d - %B - %Y | %H : %M (GMT)')}", inline=False)
                else:
                    embed.add_field(name="Invite", value=f"**URL:** {invite.url}\n**Inviter:** {invite.inviter.mention} | {invite.inviter}\n**Uses:** {invite.uses}", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            log_channel = self.guild.get_channel(249313961458008065)
            await log_channel.send(embed=embed)

    async def on_member_remove(self, member):
        if member.guild.id == 244998983112458240:
            embed = discord.Embed(title="Member Left", color=int("0xF44336", 16))
            embed.add_field(name="Member", value=f"{member} | {member}\n**ID:** `{member.id}`")
            embed.add_field(name="Joined at", value=f"{member.joined_at.strftime('%d - %B - %Y | %H : %M (GMT)')}")
            embed.add_field(name="Created at", value=f"{member.created_at.strftime('%d - %B - %Y')}")
            embed.set_thumbnail(url=member.avatar_url)
            log_channel = self.guild.get_channel(249313961458008065)
            await log_channel.send(embed=embed)

    @commands.group(hidden=True)
    async def study(self, ctx):
        """Avoid yourself from distractions and get yourself locked in study room."""
        if ctx.invoked_subcommand is None:
            role = discord.utils.get(ctx.guild.roles, id=447945813100986379)
            await ctx.author.add_roles(role, reason=ctx.author.name+" wanted to study.")
            await ctx.message.add_reaction(get_reaction_yes_no()["yes"])

    @study.command(hidden=True)
    async def stop(self, ctx):
        """Done studying or wanna take some rest? Use this command to join back the real fun."""
        role = discord.utils.get(ctx.guild.roles, id=447945813100986379)
        await ctx.author.remove_roles(role, reason=ctx.author.name+" stopped studying.")
        await ctx.message.add_reaction(get_reaction_yes_no()["yes"])

    @commands.command(name="doggo")
    @checks.is_mod()
    async def doghouse(self, ctx, member: discord.Member, *, reason: str=None):
        """Put bad doggo into jail."""
        if not reason:
            reason = "Reason not specified"
        role = discord.utils.get(ctx.guild.roles, id=396570360054677507)
        await member.add_roles(role, reason=reason)
        await ctx.message.add_reaction('✅')
        log = discord.Embed(title="🐕 | Case", color=get_random_embed_color(), timestamp=ctx.message.created_at)
        log_channel = self.guild.get_channel(408189687329456128)
        await log.add_field(name="Name", value=f"{member.name} | {member.mention}")
        await log.add_field(name="ID", value=f"`member.id`")
        await log.add_field(name="Reason", value=reason)
        await log.add_field(name="Moderator", value=f"{ctx.author.mention} | {ctx.author.name}")
        await log.set_author(name=member.name, icon_url=member.avatar_url)
        await log_channel.send(embed=log)
        

def setup(bot):
    bot.add_cog(TAD(bot))
