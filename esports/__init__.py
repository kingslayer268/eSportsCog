from .esports import esports


def setup(bot):
    cog = esports(bot)
    await cog.crtoken()
    bot.add_cog(cog)
