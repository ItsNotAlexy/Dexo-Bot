import json
import os
import nextcord
from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext import commands


with open("config/botconf.json") as f:
    config = json.load(f)

class EvalModal(nextcord.ui.Modal):
    def __init__(self, bot):
        super().__init__(
            "Eval Command",
            timeout=60
        )

        self.bot = bot

        self.code = nextcord.ui.TextInput(
            label="Code to evaluate:",
            placeholder="Enter code here",
            style=nextcord.TextInputStyle.paragraph,
            min_length=1,
            max_length=1800,
            required=True
        )
        self.add_item(self.code)

    async def callback(self, interaction: Interaction) -> None:
        code = self.code.value
        local_vars = {
            "self": self,
            "interaction": interaction,
            "bot": self.bot,
            "nextcord": nextcord,
            "commands": commands,
            "config": config,
            "os": os
        }

        try:
            exec(f"async def __ex(self, inter, bot):\n    {code}", {}, local_vars)
            result = await local_vars["__ex"](self, interaction, self.bot)
        except Exception as e:
            result = f"```{e}```"

        if result is not None:
            result = f"```{result}```"
        else:
            result = "Executed successfully with no result."

        e = nextcord.Embed(
            title="Eval Result",
            description=result,
            color=nextcord.Color.green()
        )
        try:
            await interaction.response.send_message(embed=e, ephemeral=True)
        except nextcord.errors.InteractionResponded:
            await interaction.followup.send(embed=e, ephemeral=True)


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.developers = config["DEVELOPERS"]

    @slash_command(name="reload", description="[DEV] Reloads a cog")
    async def reload(self, inter:Interaction, cog : str = SlashOption("cog", "The cog to reload", True)):
        if inter.user.id not in self.developers:
            return await inter.response.send_message("❌ | You are not authorized to use this command", ephemeral=True)
        
        try:
            self.bot.reload_extension(f"commands.{cog}")
            await inter.response.send_message(f"Reloaded `{cog}` successfully", ephemeral=True)
            print(f"COG RELOADED: {cog}")
        except Exception as e:
            await inter.response.send_message(f"Failed to reload {cog}\n```{e}```", ephemeral=True)

    @reload.on_autocomplete("cog")
    async def reload_autocomplete(self, inter:Interaction, cog: str):
        cogs = [cog for cog in os.listdir("commands") if cog.endswith(".py")]
        cogs = [cog[:-3] for cog in cogs]

        if not cog:
            return await inter.response.send_autocomplete(cogs)
        
        get_near_matches = [cog for cog in cogs if cog.startswith(cog)]
        if get_near_matches:
            return await inter.response.send_autocomplete(get_near_matches)

    @slash_command(name="unload", description="[DEV] Unloads a cog")
    async def unload(self, inter:Interaction, cog:str):
        if inter.user.id not in self.developers:
            return await inter.response.send_message("❌ | You are not authorized to use this command", ephemeral=True)
        
        try:
            self.bot.unload_extension(f"commands.{cog}")
            await inter.response.send_message(f"Unloaded `{cog}` successfully", ephemeral=True)
            print(f"COG UNLOADED: {cog}")
        except Exception as e:
            await inter.response.send_message(f"Failed to unload {cog}\n```{e}```", ephemeral=True)

    @unload.on_autocomplete("cog")
    async def unload_autocomplete(self, inter:Interaction, cog: str):
        cogs = [cog for cog in os.listdir("commands") if cog.endswith(".py")]
        cogs = [cog[:-3] for cog in cogs]

        if not cog:
            return await inter.response.send_autocomplete(cogs)
        
        get_near_matches = [cog for cog in cogs if cog.startswith(cog)]
        if get_near_matches:
            return await inter.response.send_autocomplete(get_near_matches)

    @slash_command(name="load", description="[DEV] Loads a cog")
    async def load(self, inter:Interaction, cog:str):
        if inter.user.id not in self.developers:
            return await inter.response.send_message("❌ | You are not authorized to use this command", ephemeral=True)
        
        try:
            self.bot.load_extension(f"commands.{cog}")
            await inter.response.send_message(f"Loaded `{cog}` successfully", ephemeral=True)
            print(f"COG LOADED: {cog}")
        except Exception as e:
            await inter.response.send_message(f"Failed to load {cog}\n```{e}```", ephemeral=True)

    @load.on_autocomplete("cog")
    async def load_autocomplete(self, inter:Interaction, cog: str):
        cogs = [cog for cog in os.listdir("commands") if cog.endswith(".py")]
        cogs = [cog[:-3] for cog in cogs]

        if not cog:
            return await inter.response.send_autocomplete(cogs)
        
        get_near_matches = [cog for cog in cogs if cog.startswith(cog)]
        if get_near_matches:
            return await inter.response.send_autocomplete(get_near_matches)
        

    @slash_command(name="eval", description="[DEV] Evaluates a code")
    async def eval(self, inter:Interaction):
        if inter.user.id not in self.developers:
            return await inter.response.send_message("❌ | You are not authorized to use this command", ephemeral=True)
        
        await inter.response.send_modal(EvalModal(self.bot))


def setup(bot):
    bot.add_cog(DevCommands(bot))
