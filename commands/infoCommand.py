import nextcord, psutil, vt
from datetime import datetime, timedelta
from nextcord import slash_command, Interaction
from nextcord.ext import commands


class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="info", description="Get information about the bot.")
    async def info(self, inter: Interaction):
        uptime = datetime.now() - self.bot.start_time
        formatted_uptime = str(timedelta(seconds=int(uptime.total_seconds())))
        e = nextcord.Embed(
            title="About Dexo",
            description="Dexo is a modern security bot that is designed to keep your server safe from malicious activities.",
            color=nextcord.Color.dark_theme(),
        )
        e.add_field(
            name="Uptime",
            value=f"`{formatted_uptime}`",
        )
        e.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        e.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%")
        e.add_field(name="Nextcord Version", value=f"`{nextcord.__version__}`")
        e.add_field(name="SDK Version", value=f"`{vt.__version__}`")
        e.add_field(name="Guilds", value=f"{len(self.bot.guilds)}")
        e.set_thumbnail(url=self.bot.user.avatar.url)
        e.set_footer(text="Made with ❤️ by alexyssh")

        await inter.response.send_message(embed=e)


def setup(bot):
    bot.add_cog(InfoCommands(bot))
