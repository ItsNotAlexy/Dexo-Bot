import nextcord
from nextcord.ext import commands


class AntiAltAccount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if member.bot:
            return

        guild = member.guild
        findGuildConfig = await self.db.GuildConfig.find({"guildid": guild.id})

        if not findGuildConfig:
            return

        if findGuildConfig["anti_alt_account"]:
            created_at = member.created_at
            time_difference = nextcord.utils.utcnow() - created_at

            if time_difference.days < 3:
                e = nextcord.Embed(
                    title="Dexo | Anti Alt Account",
                    description=f"{member.mention} has been detected as an alt account and has been kicked.\nMember account was created {time_difference.days} days ago.",
                    color=nextcord.Color.red()
                )
                log_channel = guild.get_channel(findGuildConfig["log_channel"])
                await member.kick(reason="Alt Account Detected")
                await log_channel.send(embed=e)
            else:
                return
            
def setup(bot):
    bot.add_cog(AntiAltAccount(bot))