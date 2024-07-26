import nextcord
from nextcord.ext import commands
from utils.dbManager import DBManager


class AntiChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()
        self.deleted_channels = {}

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: nextcord.abc.GuildChannel):
        guild_id = channel.guild.id

        if guild_id not in self.deleted_channels:
            self.deleted_channels[guild_id] = {}

        self.deleted_channels[guild_id][channel.id] = {
            'name': channel.name,
            'type': channel.type,
            'position': channel.position,
            'category': channel.category_id if isinstance(channel.category, nextcord.CategoryChannel) else None
        }

        time_window = 60
        threshold = 3

        if len(self.deleted_channels[guild_id]) > threshold:
            member = await self.get_channel_deletor(channel)
            if member:
                await self.take_action(channel.guild, member)

    async def get_channel_deletor(self, channel: nextcord.abc.GuildChannel):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_delete):
            if entry.target.id == channel.id:
                return entry.user
        return None

    async def take_action(self, guild: nextcord.Guild, member: nextcord.Member):
        findGuildConfig = await self.db.GuildConfigfind({"guildid": guild.id})

        if member == self.bot.user:
            return

        await self.restore_deleted_channels(guild)
        await member.ban(reason="Dexo Anti-Raid | Excessive Channel Deletion")

        if findGuildConfig:
            if findGuildConfig["log_channel"]:
                logChannel = guild.get_channel(findGuildConfig["log_channel"])
                e = nextcord.Embed(
                    title="Anti-Spam | Channel Deletion Spam Detected",
                    description=f"More than 3 channels were deleted in the last 60 seconds by {member.mention}, action taken to prevent further damage.",
                    color=nextcord.Color.dark_theme()
                )
                e.timestamp = nextcord.utils.utcnow()
                try:
                    await logChannel.send(embed=e)
                except AttributeError:
                    pass

    async def restore_deleted_channels(self, guild: nextcord.Guild):
        for channel_id, details in list(self.deleted_channels.get(guild.id, {}).items()):
            category_id = details.get('category')
            position = details['position']
            name = details['name']
            channel_type = details['type']

            category = None
            
            try:
                if category_id:
                    category = guild.get_channel(category_id)
                    if not category:
                        print(f"Category with ID {category_id} does not exist. Skipping category restoration.")

                if category:
                    if channel_type == nextcord.ChannelType.text:
                        await guild.create_text_channel(
                            name=name,
                            category=category,
                            position=position,
                            reason="Dexo Anti-Raid | Restoring deleted channel"
                        )
                    elif channel_type == nextcord.ChannelType.voice:
                        await guild.create_voice_channel(
                            name=name,
                            category=category,
                            position=position,
                            reason="Dexo Anti-Raid | Restoring deleted channel"
                        )
                else:
                    if channel_type == nextcord.ChannelType.text:
                        await guild.create_text_channel(
                            name=name,
                            position=position,
                            reason="Dexo Anti-Raid | Restoring deleted channel"
                        )
                    elif channel_type == nextcord.ChannelType.voice:
                        await guild.create_voice_channel(
                            name=name,
                            position=position,
                            reason="Dexo Anti-Raid | Restoring deleted channel"
                        )

                print(f"Restored channel: {name} (Category: {category.name if category else 'None'})")
                self.deleted_channels[guild.id].pop(channel_id) 
            except nextcord.HTTPException as e:
                print(f"Error restoring channel '{name}': {e.text}")
            except Exception as e:
                print(f"Error restoring channel '{name}': {e}")

def setup(bot):
    bot.add_cog(AntiChannelDelete(bot))
