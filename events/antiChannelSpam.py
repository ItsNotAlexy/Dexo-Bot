import nextcord
from nextcord.ext import commands
from utils.dbManager import DBManager
import time
from datetime import datetime, timedelta, timezone


class AntiChannelSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()
        self.channel_creation_log = {}

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: nextcord.abc.GuildChannel):
        guild_id = channel.guild.id
        current_time = time.time()

        if guild_id not in self.channel_creation_log:
            self.channel_creation_log[guild_id] = []

        self.channel_creation_log[guild_id].append(current_time)

        time_window = 60
        threshold = 3

        self.channel_creation_log[guild_id] = [
            timestamp for timestamp in self.channel_creation_log[guild_id]
            if current_time - timestamp <= time_window
        ]

        if len(self.channel_creation_log[guild_id]) > threshold:
            member = await self.get_channel_creator(channel)
            if member:
                await self.take_action(channel.guild, member)

    async def get_channel_creator(self, channel: nextcord.abc.GuildChannel):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create):
            if entry.target.id == channel.id:
                return entry.user
        return None

    async def take_action(self, guild: nextcord.Guild, member: nextcord.Member):
        findGuildConfig = await self.db.GuildConfigfind({"guildid": guild.id})

        if member == self.bot.user:
            return

        await member.ban(reason="Dexo Anti-Raid | Excessive Channel Creation")
        await self.delete_recent_channels(guild, member)

        if findGuildConfig:
            if findGuildConfig["log_channel"]:
                logChannel = guild.get_channel(findGuildConfig["log_channel"])
                e = nextcord.Embed(
                    title="Anti-Spam | Channel Creation Spam Detected",
                    description=f"More than 3 channels were created in the last 60 seconds by {member.mention}, action taken to prevent further damage.",
                    color=nextcord.Color.dark_theme()
                )
                e.timestamp = nextcord.utils.utcnow()
                await logChannel.send(embed=e)

    async def delete_recent_channels(self, guild: nextcord.Guild, member: nextcord.Member):
        time_window = timedelta(seconds=60)
        now = datetime.now(timezone.utc)

        async for entry in guild.audit_logs(limit=100, action=nextcord.AuditLogAction.channel_create):
            if entry.user.id == member.id and (now - entry.created_at) <= time_window:
                channel = entry.target
                if isinstance(channel, nextcord.abc.GuildChannel):
                    try:
                        await channel.delete(reason="Dexo Anti-Raid | Excessive Channel Creation")
                    except nextcord.errors.NotFound:
                        pass

def setup(bot):
    bot.add_cog(AntiChannelSpam(bot))
