import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from utils.dbManager import DBManager


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()

    @slash_command(name="ban", description="Ban a user from the server.")
    async def ban(
        self,
        inter: Interaction,
        user: nextcord.Member,
        reason: str = "No reason provided.",
    ):
        if not inter.author.guild_permissions.ban_members:
            return await inter.response.send_message(
                "❌ | You don't have permission to use this command.", ephemeral=True
            )

        if user.top_role >= inter.guild.me.top_role:
            return await inter.response.send_message(
                "❌ | I can't ban this user because they have a higher role than me.",
                ephemeral=True,
            )

        if inter.user.top_role <= user.top_role:
            return await inter.response.send_message(
                "❌ | You can't ban this user because they have a higher role than you.",
                ephemeral=True,
            )

        await user.ban(reason=reason)
        await inter.response.send_message(
            f"✅ | {user.mention} has been banned from the server."
        )

    @slash_command(name="kick", description="Kick a user from the server.")
    async def kick(
        self,
        inter: Interaction,
        user: nextcord.Member,
        reason: str = "No reason provided.",
    ):
        if not inter.author.guild_permissions.kick_members:
            return await inter.response.send_message(
                "❌ | You don't have permission to use this command.", ephemeral=True
            )

        if user.top_role >= inter.guild.me.top_role:
            return await inter.response.send_message(
                "❌ | I can't kick this user because they have a higher role than me.",
                ephemeral=True,
            )

        if inter.user.top_role <= user.top_role:
            return await inter.response.send_message(
                "❌ | You can't kick this user because they have a higher role than you.",
                ephemeral=True,
            )

        await user.kick(reason=reason)
        await inter.response.send_message(
            f"✅ | {user.mention} has been kicked from the server."
        )

    @slash_command(name="mute", description="Mute a user in the server.")
    async def mute(
        self,
        inter: Interaction,
        user: nextcord.Member,
        time: int,
        reason: str = "No reason provided.",
    ):
        if not inter.author.guild_permissions.manage_roles:
            return await inter.response.send_message(
                "❌ | You don't have permission to use this command.", ephemeral=True
            )

        if user.top_role >= inter.guild.me.top_role:
            return await inter.response.send_message(
                "❌ | I can't mute this user because they have a higher role than me.",
                ephemeral=True,
            )

        if inter.user.top_role <= user.top_role:
            return await inter.response.send_message(
                "❌ | You can't mute this user because they have a higher role than you.",
                ephemeral=True,
            )

        muted_role = await self.db.GuildConfig.find_one({"guildid": inter.guild.id})
        if not muted_role:
            return await inter.response.send_message(
                "❌ | Muted role has not been set up in the server.", ephemeral=True
            )

        await user.timeout(timeout=time, reason=reason)
        await inter.response.send_message(
            f"✅ | {user.mention} has been muted for {time} seconds."
        )

    @slash_command(name="unmute", description="Unmute a user in the server.")
    async def unmute(self, inter: Interaction, user: nextcord.Member):
        if not inter.author.guild_permissions.manage_roles:
            return await inter.response.send_message(
                "❌ | You don't have permission to use this command.", ephemeral=True
            )

        if user.top_role >= inter.guild.me.top_role:
            return await inter.response.send_message(
                "❌ | I can't unmute this user because they have a higher role than me.",
                ephemeral=True,
            )

        if inter.user.top_role <= user.top_role:
            return await inter.response.send_message(
                "❌ | You can't unmute this user because they have a higher role than you.",
                ephemeral=True,
            )

        await user.timeout(timeout=0, reason="Unmuted by moderator.")
        await inter.response.send_message(f"✅ | {user.mention} has been unmuted.")


def setup(bot):
    bot.add_cog(ModCommands(bot))
