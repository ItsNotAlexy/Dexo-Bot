import nextcord
from nextcord.ext import commands
from utils.raidUtils import isSpam
from utils.dbManager import DBManager
import time
from collections import defaultdict

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()
        self.message_log = defaultdict(lambda: defaultdict(list))

    @commands.Cog.listener()
    async def on_message(self, msg: nextcord.Message):
        if msg.author == self.bot.user:
            return

        guild_id = msg.guild.id
        user_id = msg.author.id
        current_time = time.time()

        self.message_log[guild_id][user_id].append((current_time, msg))

        self.message_log[guild_id][user_id] = [
            (timestamp, message) for timestamp, message in self.message_log[guild_id][user_id]
            if current_time - timestamp <= 60
        ]

        if len(self.message_log[guild_id][user_id]) > 5:
            await self.take_action(guild_id, user_id)

        await self.bot.process_commands(msg)

    async def take_action(self, guild_id: int, user_id: int):
        try:
            messages_to_delete = [msg for timestamp, msg in self.message_log[guild_id][user_id]]

            for msg in messages_to_delete:
                await msg.delete()

            self.message_log[guild_id][user_id] = []

            findGuildConfig = await self.db.GuildConfigfind({"guildid": guild_id})
            if findGuildConfig and findGuildConfig["log_channel"]:
                logChannel = self.bot.get_channel(findGuildConfig["log_channel"])
                user = self.bot.get_user(user_id)
                if user:
                    e = nextcord.Embed(
                        title="Anti-Raid | Spam Detected",
                        description=f"User: {user.mention}\nMessages deleted to prevent spam.",
                        color=nextcord.Color.dark_theme()
                    )
                    e.set_footer(text="User has been banned and messages were deleted.")
                    await logChannel.send(embed=e)

                member = await msg.guild.fetch_member(user_id)
                await member.ban(reason="Dexo Anti-Raid | Spam detected.")

        except Exception as e:
            print(f"Error handling spam: {e}")

def setup(bot):
    bot.add_cog(AntiSpam(bot))
