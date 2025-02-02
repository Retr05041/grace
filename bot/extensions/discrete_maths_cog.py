from discord.ext.commands import Cog, hybrid_group, Context
from bot.extensions.command_error_handler import CommandErrorHandler
from bot.helpers.error_helper import get_original_exception

import lib.discrete_maths.logic_operations as logic_operations

class DiscreteMathsCog(Cog, name="Discrete Maths", description="Run discrete maths commands."):
    """A Discord Cog that allows descrite maths concepts to be ran as commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @hybrid_group(name="dm", help="Discrete Maths commands")
    async def discrete_maths_group(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await CommandErrorHandler.send_command_help(ctx)
    
    @discrete_maths_group.command(name="truth_table", aliases=['tt'], help="Input a proposition and get a truth table. example: \"(~A v B) ^ S\"", usage="\"{proposition}\"")
    async def truth_table_command(self, ctx: Context, proposition: str) -> None:
        await ctx.send(f"Truth table: ```{logic_operations.create_truth_table(proposition)}```")

    @discrete_maths_group.command(name="is_tautology", aliases=['it'], help="Input a proposition and check if it is a tautology. example: \"(~A v B) ^ S\"", usage="\"{proposition}\"")
    async def tautology_checker_command(self, ctx: Context, proposition: str) -> None:
        if (logic_operations.is_prop_tautolgy(proposition)):
            await ctx.send(f"It's a tautology.")
        else:
            await ctx.send(f"It's not a tautology.")

    @discrete_maths_group.error
    async def discrete_maths_command_error(self, ctx: Context, error) -> None:
        error = get_original_exception(error)
        await ctx.send(f"Error: {error}", ephemeral=True)
    
    
async def setup(bot):
    await bot.add_cog(DiscreteMathsCog(bot))