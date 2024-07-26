import nextcord
from nextcord.ext import commands
from utils.dbManager import DBManager


class MemberJoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        findConfig = await self.db.GuildConfigfind({"guildid": member.guild.id})

        if findConfig["verify_members"] == True:
            try:
                e = nextcord.Embed(
                    title="Verification Required!",
                    description="Please use the command </verify:1249200891110621214> to verify yourself in the server.",
                    color=nextcord.Color.dark_theme(),
                )
                e.set_footer(text="Server Protected by Dexo")
                e.timestamp = nextcord.utils.utcnow()
                await member.send(embed=e)
            except nextcord.Forbidden:
                pass
        else:
            return


def setup(bot):
    bot.add_cog(MemberJoins(bot))
