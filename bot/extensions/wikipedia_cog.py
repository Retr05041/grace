from discord.ext.commands import Cog, hybrid_command
import discord
from urllib.request import urlopen
from urllib.parse import quote_plus
from json import loads


def search_results(search):
        url_encode = quote_plus(search)
        url = "https://en.wikipedia.org/w/api.php?action=opensearch" \
              "&format=json&limit=3&namespace=0&search=" + url_encode
        with urlopen(url) as url:
            return loads(url.read())


class Buttons(discord.ui.View):
    def __init__(self, search, result):
        super().__init__()
        self.search = search
        self.result = result
        self.value = None

    @discord.ui.button(label='1', style=discord.ButtonStyle.primary)
    async def first_wiki_result(self, interaction: discord.Interaction,
                                button: discord.ui.Button):
        if (len(self.result[3]) >= 1):
            await interaction.response.send_message(interaction.user.mention
                                                    + " requested:\n"
                                                    + self.result[3][0])
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message("Invalid choice.",
                                                    ephemeral=True)

    @discord.ui.button(label='2', style=discord.ButtonStyle.primary)
    async def second_wiki_result(self, interaction: discord.Interaction,
                                 button: discord.ui.Button):
        if (len(self.result[3]) >= 2):
            await interaction.response.send_message(interaction.user.mention
                                                    + " requested:\n"
                                                    + self.result[3][1])
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message("Invalid choice.",
                                                    ephemeral=True)

    @discord.ui.button(label='3', style=discord.ButtonStyle.primary)
    async def third_wiki_result(self, interaction: discord.Interaction,
                                button: discord.ui.Button):
        if (len(self.result[3]) == 3):
            await interaction.response.send_message(interaction.user.mention
                                                    + " requested:\n"
                                                    + self.result[3][2])
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message("Invalid choice.",
                                                    ephemeral=True)


class Wikipedia(Cog, name="Wikipedia", description="Search on Wikipedia."):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(
        description="Searches and displays the first 3 results "
                    "from Wikipedia.")
    async def wiki(self, ctx, search: str):
        result = search_results(search)
        view = Buttons(search, result)
        if (len(result[1]) == 0):
            await ctx.interaction.response.send_message("No result found.",
                                                        ephemeral=True)
        else:
            resultView = ""
            search_count = 1
            for result in result[1]:
                resultView += str(search_count) + ": " + result + "\n"
                search_count += 1
            await ctx.send(resultView, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Wikipedia(bot))
