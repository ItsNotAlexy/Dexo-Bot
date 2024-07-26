import nextcord, json, vt
from nextcord.ext import commands
from urllib.parse import urlparse
from utils.dbManager import DBManager
from datetime import timedelta


with open("config/apiconf.json") as f:
    config = json.load(f)


class MessageRuntime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()

    @commands.Cog.listener()
    async def on_message(self, message):
        msgContent = message.content

        if (
            "https://" in msgContent
            or "http://" in msgContent
            or ("<" in msgContent and ">" in msgContent)
        ):
            url_start = msgContent.find("http")
            url_end = msgContent.find(" ", url_start)
            full_url = (
                msgContent[url_start:url_end]
                if url_end != -1
                else msgContent[url_start:]
            )
            parsed_url = urlparse(full_url)
            domain_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

            if domain_url:
                vtClient = vt.Client(config["VT_API_KEY"])
                link_id = vt.url_id(domain_url)

                try:
                    await vtClient.scan_url_async(domain_url)
                    scan_object = await vtClient.get_json_async(f"/urls/{link_id}")

                    if (
                        scan_object["data"]["attributes"]["last_analysis_stats"][
                            "malicious"
                        ]
                        >= 1
                    ):
                        await message.delete()
                        findLogChannel = await self.db.GuildConfigfind(
                            {"guildid": message.guild.id}
                        )

                        if findLogChannel:
                            logChannel = message.guild.get_channel(
                                findLogChannel["log_channel"]
                            )
                            e = nextcord.Embed(
                                title="Malicious Link Detected!",
                                description=f"A malicious link was detected in {message.channel.mention} and was deleted.",
                                color=nextcord.Color.dark_theme(),
                            )
                            e.add_field(name="Sender", value=message.author.mention)
                            e.add_field(name="Sender ID", value=message.author.id)
                            e.add_field(
                                name="Scan ID",
                                value=f'`{scan_object["data"]["id"]}`',
                                inline=False,
                            )
                            e.add_field(
                                name="Scan Link",
                                value=f"[Click Here](https://www.virustotal.com/gui/url/{link_id}/detection)",
                            )
                            e.set_author(
                                name=message.author, icon_url=message.author.avatar.url
                            )
                            e.set_footer(text="Powered by VirusTotal™️")
                            e.timestamp = message.created_at
                            await logChannel.send(embed=e)

                            getUserRecords = await self.db.findUserWarn(
                                {"userid": message.author.id}
                            )
                            getMutedAfter = await self.db.GuildConfigfind(
                                {"guildid": message.guild.id}
                            )
                            getMutedFor = await self.db.GuildConfigfind(
                                {"guildid": message.guild.id}
                            )

                            if not getUserRecords:
                                await self.db.addUserWarn(
                                    {
                                        "guildid": message.guild.id,
                                        "userid": message.author.id,
                                        "warns": 0,
                                    }
                                )

                            if getUserRecords >= getMutedAfter["mute_after"]:
                                try:
                                    await message.author.timeout(
                                        timedelta(
                                            minutes=int(getMutedFor["muted_time"])
                                        ),
                                        reason="Automated Mute",
                                    )
                                    await message.author.send(
                                        f"You were muted in {message.guild.name} for sending a malicious link. If you believe this was a mistake, please contact the server staff."
                                    )
                                    await self.db.updateUserWarn(
                                        {"userid": message.author.id}, {"warns": 0}
                                    )
                                except nextcord.errors.Forbidden:
                                    return
                            else:
                                await self.db.updateUserWarn(
                                    {"userid": message.author.id},
                                    {"warns": getUserRecords["warns"] + 1},
                                )
                                await message.author.send(
                                    f"Please refrain from sending malicious links in {message.guild.name}. You have {getMutedAfter - getUserRecords['warns']} warnings left before you are muted."
                                )
                                return
                        else:
                            getUserRecords = await self.db.getUserWarns(
                                {"userid": message.author.id}
                            )
                            getMutedAfter = await self.db.find(
                                {"guildid": message.guild.id}
                            )
                            getMutedFor = await self.db.GuildConfigfind(
                                {"guildid": message.guild.id}
                            )

                            if not getUserRecords:
                                await self.db.addUserWarn(
                                    {
                                        "guildid": message.guild.id,
                                        "userid": message.author.id,
                                        "warns": 0,
                                    }
                                )

                            if getUserRecords >= getMutedAfter["mute_after"]:
                                try:
                                    await message.author.timeout(
                                        timedelta(int(getMutedFor["muted_time"])),
                                        reason="Automated Mute",
                                    )
                                    await message.author.send(
                                        f"You were muted in {message.guild.name} for sending a malicious link. If you believe this was a mistake, please contact the server staff."
                                    )
                                    await self.db.updateUserWarn(
                                        {"userid": message.author.id}, {"warns": 0}
                                    )
                                except nextcord.errors.Forbidden:
                                    return
                            else:
                                await self.db.updateUserWarn(
                                    {"userid": message.author.id},
                                    {"warns": getUserRecords["warns"] + 1},
                                )
                                await message.author.send(
                                    f"Please refrain from sending malicious links in {message.guild.name}. You have {getMutedAfter - getUserRecords['warns']} warnings left before you are muted."
                                )
                                return
                    else:
                        return
                except vt.error.APIError:
                    return
            else:
                return
        else:
            return


def setup(bot):
    bot.add_cog(MessageRuntime(bot))
