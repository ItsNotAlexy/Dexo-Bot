import nextcord
import random
import os
from captcha.image import ImageCaptcha
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from utils.dbManager import DBManager


class VerifyButtons(nextcord.ui.View):
    def __init__(self, correct_value, random_values):
        super().__init__()
        self.correct_value = correct_value
        self.buttons_info = {}
        self.db = DBManager()

        all_values = list(set(random_values))
        if correct_value not in all_values:
            all_values.append(correct_value)
        all_values = all_values[:3]

        random.shuffle(all_values)

        for value in all_values:
            custom_id = f"verify_button_{value}"
            self.buttons_info[custom_id] = value == correct_value
            button = nextcord.ui.Button(
                label=value, style=nextcord.ButtonStyle.primary, custom_id=custom_id
            )
            button.callback = self.handle_button_click
            self.add_item(button)

    async def handle_button_click(self, inter: Interaction):
        get_customId = inter.data["custom_id"]
        splitCustomId = get_customId.split("_")

        if self.correct_value == splitCustomId[-1]:
            findRoleConfig = await self.db.GuildConfigfind({"guildid": inter.guild.id})
            if findRoleConfig:
                findRole = inter.guild.get_role(findRoleConfig["verified_role"])
                await inter.user.add_roles(findRole)
            await inter.response.send_message(
                "You have successfully verified yourself!", ephemeral=True
            )
            self.stop()
        else:
            await inter.response.send_message(
                "You have selected the wrong captcha. Please try again.", ephemeral=True
            )
            self.stop()

    async def on_timeout(self, inter: Interaction):
        return await inter.response.send_message(
            "This button has timed out, Please try again.", ephemeral=True
        )


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBManager()

    @slash_command(
        name="verify", description="Verify yourself to get access to the server."
    )
    async def verify(self, inter: Interaction):
        findRoleConfig = await self.db.GuildConfigfind({"guildid": inter.guild.id})
        if inter.user.bot:
            return

        if inter.user.get_role(findRoleConfig["verified_role"]):
            return await inter.response.send_message(
                "❌ | You are already verified!", ephemeral=True
            )

        generate_random_int = random.randint(1000, 9999)
        correct_value = str(generate_random_int)
        image = ImageCaptcha(width=280, height=90)

        image_file_path = f"captcha_{correct_value}.png"
        image.write(correct_value, image_file_path)

        e = nextcord.Embed(
            title="Captcha Verification",
            description="Please select the correct captcha to prove that you are not a robot.",
            color=nextcord.Color.dark_theme(),
        )
        e.set_image(url=f"attachment://{image_file_path}")
        await inter.send(
            embed=e,
            file=nextcord.File(image_file_path),
            view=VerifyButtons(
                correct_value, [str(random.randint(1000, 9999)) for _ in range(2)]
            ),
            ephemeral=True,
        )
        os.remove(image_file_path)


def setup(bot):
    bot.add_cog(Verify(bot))
