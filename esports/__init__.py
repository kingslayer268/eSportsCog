from .esports import esports


def setup(bot):
    cog = esports(bot)
    bot.add_cog(cog)
