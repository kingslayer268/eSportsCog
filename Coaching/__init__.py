from .coaching import Coaching


def setup(bot):
    bot.add_cog(Coaching(bot))
