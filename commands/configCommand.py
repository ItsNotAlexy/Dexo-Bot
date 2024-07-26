import nextcord
import random
from utils.dbManager import DBManager
from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext import commands


class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()

    @slash_command(name="config", description="Configure the bot.")
    async def config(self, inter: Interaction):
        pass

    @config.subcommand(
        name="view",
        description="View the current settings of the bot."
    )
    async def viewConfig(self, inter: Interaction):
        try:
            e = nextcord.Embed(title="Bot Configuration", color=nextcord.Color.dark_theme())
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                config_mapping = {
                    "log_channel": ("📜 Log Channel", True),
                    "mute_after": ("🔇 Mute After", False),
                    "mute_time": ("⌛ Mute Time", True),
                    "verify_members": ("❓ Verify Members", False),
                    "verified_role": ("✅ Verified Role", True)
                }

                for key, (display_name, inline) in config_mapping.items():
                    if key in getRecords:
                        if key == "log_channel":
                            value = f"<#{getRecords[key]}>" if getRecords[key] else "None"
                            inline = False
                        elif key == "verified_role":
                            value = f"<@&{getRecords[key]}>" if getRecords[key] else "None"
                        elif key == "verify_members":
                            value = "Enabled" if getRecords[key] else "Disabled"
                        elif key == "mute_time":
                            value = f"`{getRecords[key]}` minutes" if getRecords[key] else "None"
                        else:
                            value = f"`{getRecords[key]}` warnings" if getRecords[key] else "None"
                    else:
                        value = "None"
                    
                    e.add_field(name=display_name, value=value, inline=inline)

                await inter.response.send_message(embed=e)
            else:
                await inter.response.send_message(
                    "❌ | Bot has not been setup with settings. Please use </config setup:1248485552429207563> to setup the bot."
                )
        except Exception as e:
            await inter.response.send_message(f"❌ | An error occurred: {str(e)}", ephemeral=True)
            raise e 


    @config.subcommand(
        name="setup",
        description="Set's up the bot with all settings set to False/None.",
    )
    async def setupConfig(self, inter: Interaction):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                return await inter.response.send_message(
                    "❌ | Bot has already been setup with settings."
                )
            else:
                await self.db.GuildConfiginsert(
                    {
                        "guildid": inter.guild.id,
                        "log_channel": None,
                        "mute_after": None,
                        "mute_time": None,
                        "verify_members": False,
                        "verified_role": None,
                    }
                )
                return await inter.response.send_message(
                    "✅ | Bot has been setup with all settings set to False/None."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )

    @config.subcommand(name="reset", description="Resets the bot settings.")
    async def resetConfig(self, inter: Interaction):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                await self.db.GuildConfigupdate(
                    {"guildid": inter.guild.id},
                    {
                        "guildid": inter.guild.id,
                        "log_channel": None,
                        "mute_after": None,
                        "mute_time": None,
                        "verify_members": False,
                        "verified_role": None,
                    }
                )
                return await inter.response.send_message(
                    "✅ | Bot settings have been reset."
                )
            else:
                return await inter.response.send_message(
                    "❌ | Bot has not been setup with settings."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )

    @config.subcommand(name="log_channel", description="Set logging channel.")
    async def logChannelConfig(self, inter: Interaction, channel: nextcord.TextChannel):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                await self.db.GuildConfigupdate(
                    {"guildid": inter.guild.id}, {"log_channel": channel.id}
                )
                return await inter.response.send_message(
                    f"✅ | Log channel has been set to **{channel.mention}**."
                )
            else:
                await self.db.GuildConfiginsert(
                    {"guildid": inter.guild.id, "log_channel": channel.id}
                )
                return await inter.response.send_message(
                    f"✅ | Log channel has been set to **{channel.mention}**."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )

    @config.subcommand(
        name="mute_after",
        description="Sets a user to be muted after a certain amount of warnings.",
    )
    async def muteAfterConfig(self, inter: Interaction, warnings: int):
        if inter.user.guild_permissions.manage_guild:
            if warnings < 1:
                return await inter.response.send_message(
                    "❌ | The amount of warnings must be greater than 0."
                )
            elif warnings > 3:
                return await inter.response.send_message(
                    "❌ | The amount of warnings must be less than or equal to 3."
                )

            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                await self.db.GuildConfigupdate(
                    {"guildid": inter.guild.id}, {"mute_after": warnings}
                )
                return await inter.response.send_message(
                    f"✅ | User will be muted after **{warnings}** warnings."
                )
            else:
                await self.db.GuildConfiginsert(
                    {"guildid": inter.guild.id, "mute_after": warnings}
                )
                return await inter.response.send_message(
                    f"✅ | User will be muted after **{warnings}** warnings."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )

    @config.subcommand(
        name="mute_time",
        description="Sets the time for which a user will be muted for.",
    )
    async def muteTimeConfig(
        self,
        inter: Interaction,
        minutes: int = SlashOption(
            description="The amount of minutes the user will be muted for."
        ),
    ):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                await self.db.GuildConfigupdate(
                    {"guildid": inter.guild.id}, {"mute_time": minutes}
                )
                return await inter.response.send_message(
                    f"✅ | User will be muted for **{minutes}** minutes."
                )
            else:
                await self.db.GuildConfiginsert(
                    {"guildid": inter.guild.id, "mute_time": minutes}
                )
                return await inter.response.send_message(
                    f"✅ | User will be muted for **{minutes}** minutes."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )

    @config.subcommand(
        name="verify_members",
        description="Sets for all members to verify before chatting.",
    )
    async def verifyMembersConfig(
        self,
        inter: Interaction,
        option: bool = SlashOption(choices={"enabled": 1, "disabled": 0}),
    ):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if option == 1:
                try:
                    if getRecords["verify_members"] == True:
                        return await inter.response.send_message(
                            "❌ | This option is already enabled."
                        )
                    else:
                        if getRecords:
                            await self.db.GuildConfigupdate(
                                {"guildid": inter.guild.id}, {"verify_members": True}
                            )
                            return await inter.response.send_message(
                                "✅ | All members must now verify before chatting."
                            )
                        else:
                            await self.db.GuildConfiginsert(
                                {"guildid": inter.guild.id, "verify_members": True}
                            )
                            return await inter.response.send_message(
                                "✅ | All members must now verify before chatting."
                            )
                except KeyError:
                    await self.db.GuildConfigupdate(
                        {"guildid": inter.guild.id}, {"verify_members": True}
                    )
                    return await inter.response.send_message(
                        "✅ | All members must now verify before chatting."
                    )
            else:
                try:
                    if getRecords["verify_members"] == False:
                        return await inter.response.send_message(
                            "❌ | This option is already disabled."
                        )
                    else:
                        if getRecords:
                            await self.db.GuildConfigupdate(
                                {"guildid": inter.guild.id}, {"verify_members": False}
                            )
                            return await inter.response.send_message(
                                "✅ | All members no longer need to verify before chatting."
                            )
                        else:
                            await self.db.GuildConfiginsert(
                                {"guildid": inter.guild.id, "verify_members": False}
                            )
                            return await inter.response.send_message(
                                "✅ | All members no longer need to verify before chatting."
                            )
                except KeyError:
                    await self.db.GuildConfiginsert(
                        {"guildid": inter.guild.id, "verify_members": False}
                    )
                    return await inter.response.send_message(
                        "✅ | All members no longer need to verify before chatting."
                    )

    @config.subcommand(
        name="verified_role",
        description="Sets the role to be given to verified members.",
    )
    async def verifiedRoleConfig(
        self,
        inter: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to be given to verified members."
        ),
    ):
        if inter.user.guild_permissions.manage_guild:
            getRecords = await self.db.GuildConfigfind({"guildid": inter.guild.id})

            if getRecords:
                await self.db.GuildConfigupdate(
                    {"guildid": inter.guild.id}, {"verified_role": role.id}
                )
                return await inter.response.send_message(
                    f"✅ | Verified role has been set to **{role.mention}**."
                )
            else:
                await self.db.GuildConfiginsert(
                    {"guildid": inter.guild.id, "verified_role": role.id}
                )
                return await inter.response.send_message(
                    f"✅ | Verified role has been set to **{role.mention}**."
                )
        else:
            return await inter.response.send_message(
                "❌ | You don't have the required permissions to use this command.",
                ephemeral=True,
            )


def setup(bot):
    bot.add_cog(ConfigCommands(bot))
