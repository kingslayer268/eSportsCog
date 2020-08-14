from .esports import esports


async def setup(bot):
    cog = esports(bot)
    await cog.crtoken()
    bot.add_cog(cog)
