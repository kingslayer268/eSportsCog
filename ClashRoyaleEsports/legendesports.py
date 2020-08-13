import mysql.connector
import discord
import clashroyale
from redbot.core import commands, Config, checks

class LegendEsports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog("ClashRoyaleTools").constants # will I even use it?
        self.config = Config.get_conf(self, identifier=324546534)
        default_member = {"command_used": False}
        self.config.register_member(**default_member)
        
        

    async def crtoken(self):
        # Clash Royale API
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Use !set api clashroyale token,YOUR_TOKEN to set it")
        self.cr = clashroyale.official_api.Client(token=token['token'],
                                                  is_async=True,
                                                  url="https://proxy.royaleapi.dev/v1")
    
    @commands.command()
    @commands.guild_only()
    async def tryouts(self, ctx, user: discord.Member = None):
        if ctx.author == user or self.bot.is_mod(ctx.author) or user is None:
            if user is None:
                user = ctx.author
            player_tag = self.tags.getTag(userID = user.id)
            if player_tag is None:
                await ctx.send("No tag saved, use the command `!save <your tage here>`")

            else:
                try:
                    player_data = await self.cr.get_player(player_tag)
                except clashroyale.RequestError:
                    return await ctx.send("Can't reach the supercell servers at the moment")

                pb = player_data.bestTrophies
                max_wins = player_data.challengeMaxWins
                top_ladder_finisher = False
                top_global_finish = False
                ccwins = 0
                gcwins = 0

                for badge in player_data.badges: # Credit to Generaleoley 
                    if badge.name == 'Classic12Wins':
                        ccwins = badge.progress
                    elif badge.name == 'Grand12Wins':
                        gcwins = badge.progress
                    elif badge.name == "LadderTournamentTop1000_1":
                        top_global_finish = True
                    elif badge.name == "LadderTop1000_1":
                        top_ladder_finisher = True

                if (top_ladder_finisher) or ((gcwins >= 0 or ccwins >= 0) and pb >= 5300) or (top_global_finish and max_wins >= 17):
                    maintserver = self.bot.get_guild(740567594381213727)
                    channel = maintserver.get_channel(740567594381213730)
                    dm_channel = user.dm_channel
                    if dm_channel is None:
                        await user.create_dm()
                    invite = await channel.create_invite(max_uses=1)
                    embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                    embed.add_field(name="Team Eligible for:", value="Main Team", inline=True)
                    embed.add_field(name="Personal Best:", value=pb, inline=True)  
                    embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                    embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                    embed.add_field(name="Max Wins", value=max_wins, inline=True)
                    embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                    await ctx.send(embed=embed)
                    await user.send("Hey! {}, You are eligible to tryout for the LeGeND Main Team. Please join the server link given below, **DON'T SHARE IT WITH ANYONE** as its a one time link and will expire after one use.".format(user.mention))
                    await user.send(invite)
                    await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")

                elif pb >= 5600 and (ccwins >= 1 or gcwins >= 1):
                    embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                    embed.add_field(name="Team Eligible for:", value="Challenger Team", inline=True)
                    embed.add_field(name="Personal Best:", value=pb, inline=True)  
                    embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                    embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                    embed.add_field(name="Max Wins", value=max_wins, inline=True)
                    embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                    await ctx.send(embed=embed)
                    await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")

                else:
                    embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                    embed.add_field(name="Team Eligible for:", value="Academy Team", inline=True)
                    embed.add_field(name="Personal Best:", value=pb, inline=True)  
                    embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                    embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                    embed.add_field(name="Max Wins", value=max_wins, inline=True)
                    embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                    await ctx.send(embed=embed)
                    await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")
                    

                    

        else:
            await ctx.send("You are not allowed to use this commmand for other users")

            
              

    

        
