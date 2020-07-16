from redbot.core import Config, commands, checks
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import discord
import asyncio

credit = "Bot by LeGeND Gaming"


class UserEnd(Exception):
    pass


class Coaching(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=535654636546)
        default_global = {'beatdown': ["The goal is to overwhelm your opponent with a really push. It's just about stacking alot of units behind your tanks.",
                                       "Get those pumps down - In single elixir time you really want to have as many pumps as you can on the board. Each pumps gains you 2 elixir. That elixir lead really helps when you unleash those huge beatdown pushes.",
                                       "Use your tower hp as a resource which results in massive positive elixir trades, don't be afraid to trade towers.",
                                       "Don't play a tank until double elixir time if you have a heavy beatdown deck.",
                                       "Don't give up until the end because only one push can change the whole game.",
                                       "Here is Morten playing some Beatdown: https://www.youtube.com/watch?v=L9KkWq9eizo"],

                          'cycle': ["Cycle decks provide a lesson on managing constant pressure and flawless execution of defense and cycle cards",
                                    "Cycle deck’s main idea is identifying the opponent’s counters to you win con and out cycling it while keeping a steady defense",
                                    "You have to be mindful while cycling the cards and not just spam and waste the cards which can be important in defense or offense.",
                                    "You have to be cautious that you don't leak elixir and play cards proactively rarther than playing reactively.",
                                    "Here is some clean game play from Oyassu, playing one of the most used cycle deck 2.6 hog rider: https://www.youtube.com/watch?v=N5r-QN2DgMI ",
                                    ],


                          'siege': ["Siege decks teach how to avoid blind plays, how to maximize spell value, how to preplant, how to predict, when to attack and when to defend, when to resort to spell cycling",
                                    "Siege is all about counting and exploiting your elixir advantage. When you have the advantage, offensive xbow/mortar, when they have it, defensive and make trades to get ahead in the elixir count.",
                                    "If you don't know the count, do not play offensive, wait till you can work it out",
                                    "In double and triple elixir, defend and spell cycle or stack siege cards if you're up elixir",
                                    "Check out some insane xbow gameplay from crafter: https://www.youtube.com/watch?v=_cg8mrLorng "],

                          'control': ["Control decks teach how to maximize spell value, maintain constant pressure, keep up a sturdy defense, how to overcommit properly",
                                      "Control Archetype is a playstyle in which you manipulate the opponent. You defend against his/her pushes at the same time gaining elixir advantage and slowly wear him/her down by counter push and chip damage",
                                      "Control decks are filled with mostly reactive cards so you should wait for the opponent’s moves to act.",
                                      "Control deck is all about counter push value and knowing when to use building/spell in defense and when to use troops so you can build up that counter push",
                                      "A video of SirTag asserting dominance with a graveyard control deck: https://www.youtube.com/watch?v=_m8RP3hCmXE",
                                      ]}

        default_guild = {'coachid': 640859885210173450,
                         'coachchannel': 713242989245235210,
                         'neededlist': []}

        default_member = {'ign': None,
                          'tag': None,
                          'time': None,
                          'deck_type': None
                          }

        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)

    async def emb(self, ctx, title_1, title_2, title_3, title_4, title_5, value_1, value_2, value_3, value_4, value_5):
        embed = discord.Embed(color=0xFFFF00, title='Coaching Needed', description="This player needs coaching coaches please contact ASAP")
        embed.add_field(name=title_1, value=value_1)
        embed.add_field(name=title_2, value=value_2)
        embed.add_field(name=title_3, value=value_3)
        embed.add_field(name=title_4, value=value_4)
        embed.add_field(name=title_5, value=value_5)
        embed.set_footer(text=credit)
        channel_id = await self.config.guild(ctx.guild).coachchannel()
        channel = ctx.guild.get_channel(int(channel_id))
        await channel.send(embed=embed)

    @commands.group()
    @commands.guild_only()
    async def coaching(self, ctx):
        """We Got you covered for your coaching needs"""
        pass

    @coaching.command()
    @commands.guild_only()
    async def tips(self, ctx):
        """Get some tips from the bot"""
        if ctx.guild.id == 445092370006933505:
            user = ctx.author
            data = self.config

            def check(n):
                return n.author == user and n.channel == ctx.channel
            try:

                await ctx.send("{} Which Archetype's tips do you need?(Cycle, Beatdown, Control, Siege), type any ".format(ctx.author.mention))
                archatype = await self.bot.wait_for('message', timeout=60, check=check)
                final_archatype = archatype.content.lower()

                if final_archatype == "beatdown":
                    tips = await data.get_raw("beatdown")
                    await ctx.send("Use reaction menu to navigate through tips")
                    await menu(ctx, tips, DEFAULT_CONTROLS)

                elif final_archatype == "cycle":
                    tips = await data.get_raw("cycle")
                    await ctx.send("Use reaction menu to navigate through tips")
                    await menu(ctx, tips, DEFAULT_CONTROLS)

                elif final_archatype == "control":
                    tips = await data.get_raw("control")
                    await ctx.send("Use reaction menu to navigate through tips")
                    await menu(ctx, tips, DEFAULT_CONTROLS)

                elif final_archatype == "siege":
                    tips = await data.get_raw("siege")
                    await ctx.send("Use reaction menu to navigate through tips")
                    await menu(ctx, tips, DEFAULT_CONTROLS)

                else:
                    raise UserEnd

            except asyncio.exceptions.TimeoutError:
                await ctx.send("Timeout...")
                return
            except UserEnd:
                await ctx.send("Stopped!")
                return
        else:
            await ctx.send("This command only works in the Legend eSports server")

    @coaching.command()
    @commands.guild_only()
    async def coach(self, ctx):
        """Get help from a verified coach"""
        if ctx.guild.id == 445092370006933505:
            user = ctx.author
            dm_channel = user.dm_channel
            guild_data = self.config.guild(ctx.guild)
            coach_id = await guild_data.coachid()
            coach = ctx.guild.get_role(int(coach_id))
            channel_id = await self.config.guild(ctx.guild).coachchannel()
            channel = ctx.guild.get_channel(int(channel_id))
            if dm_channel is None:
                dm_channel = await user.create_dm()
            lst = await guild_data.get_raw("neededlist")
            player_data = self.config.member(ctx.author)

            def check(m):
                return m.channel == dm_channel and m.author == user

            try:
                if user.id in lst:
                    await ctx.send("You already have a coaching request pending please stay patient or contact our staff if its been over 48 hrs since your coaching request")
                else:
                    await ctx.send("Please check your DM's...")
                    await user.send("Please tell us your In game name?, Type 'stop' to stop the process")
                    ign = await self.bot.wait_for('message', timeout=60, check=check)
                    ign_use = ign.content
                    new_ign = ign.content.lower()
                    if new_ign == "stop":
                        raise UserEnd
                    await user.send("Please tell us your Player Tag?, Type 'stop' to stop the process")
                    tag = await self.bot.wait_for('message', timeout=60, check=check)
                    tag_use = tag.content
                    new_tag = tag.content.lower()
                    if new_tag == "stop":
                        raise UserEnd
                    await user.send("What time do you prefer for coaching? (Times in UTC only), Type 'stop' to stop the process")
                    time = await self.bot.wait_for('message', timeout=60, check=check)
                    time_use = time.content
                    np = time.content.lower()
                    if np == "stop":
                        raise UserEnd
                    await user.send("What archatypes do you prefer to play?")
                    deck = await self.bot.wait_for('message', timeout=60, check=check)
                    new_deck = deck.content.lower()  # I know I could have made a function to check this but my brain is not working
                    deck_use = deck.content
                    if new_deck == "stop":
                        raise UserEnd

                    await user.send("You will be contacted by one of our coaches please stay patient.")
                    await channel.send("{} New coaching request from {}".format(coach.mention, user.mention))
                    await self.emb(ctx, "Discord Name", "In Game Name", "Player Tag", "Preferred Time", "Deck Type", user.mention, ign_use, tag_use, time_use, deck_use)
                    lst.append(user.id)
                    await self.config.guild(ctx.guild).neededlist.set(lst)
                    await player_data.ign.set(ign_use)
                    await player_data.tag.set(tag_use)
                    await player_data.time.set(time_use)
                    await player_data.deck_type.set(deck_use)

            except asyncio.exceptions.TimeoutError:
                await user.send("Timeout...")  # not sure where to send these messages
                return
            except UserEnd:
                await user.send("Stopped!")  # not sure where to send these messages
                return
        else:
            await ctx.send("This command only works in the Legend eSports server")

    @commands.guild_only()
    @coaching.command()
    async def pending(self, ctx):
        """Shows how many people need coaching"""
        if ctx.guild.id == 445092370006933505:
            data = self.config.guild(ctx.guild)
            lst = await data.get_raw('neededlist')
            description = ""
            coach = await data.coachid()
            coach_role = ctx.guild.get_role(coach)
            x = ctx.author.roles
            x.pop(0)
            for roles in x:
                if roles.position >= coach_role.position:
                    for member in lst:
                        userobj = ctx.guild.get_member(int(member))
                        description += (str(userobj.mention) + '\n')
                    embed = discord.Embed(color=0xFFFF00, title='Coaching Needed by following people', description=description)
                    embed.set_footer(text=credit)
                    await ctx.send(embed=embed)
                    await ctx.send('Type "{0}coaching done @<player name>" if the player has been coached or type "{0}coaching info <@playername>" to view the details submitted by the user'.format(ctx.prefix))
                    break
                else:
                    await ctx.send("You are not allowed to do that")
                    break
        else:
            await ctx.send("This command only works in the Legend eSports server")

    @commands.guild_only()
    @coaching.command()
    async def done(self, ctx, member: discord.Member):
        """Use this only when you have successfully coached someone and the player is satisfied"""
        if ctx.guild.id == 445092370006933505:
            data = self.config.guild(ctx.guild)
            lst = await data.get_raw('neededlist')
            coach = await data.coachid()
            coach_role = ctx.guild.get_role(coach)
            x = ctx.author.roles
            x.pop(0)
            for roles in x:
                if roles.position >= coach_role.position:
                    if member.id in lst:
                        lst.remove(member.id)
                        await self.config.guild(ctx.guild).neededlist.set(lst)
                        await self.config.member(member).clear()
                        await ctx.send("Removed member from pending list")
                        break
                    else:
                        await ctx.send("Member not in the pending list")
                        break
                else:
                    await ctx.send("You are not allowed to do that")
                    break
        else:
            await ctx.send("This command only works in the Legend eSports server")


    @checks.mod_or_permissions()
    @commands.guild_only()
    @coaching.command()
    async def setcoachrole(self, ctx, role: discord.Role):
        """Sets a coach role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).coachid.set(int(id))
            await ctx.send("You set {} as the coach role id".format(role.id))
        else:
            await ctx.send("This command only works in the Legend eSports server")

    @checks.mod_or_permissions()
    @coaching.command()
    @commands.guild_only()
    async def setcoachchannel(self, ctx, channel: int):
        """Sets the channel where every request goes"""
        if ctx.guild.id == 445092370006933505:
            await self.config.guild(ctx.guild).coachchannel.set(int(channel))
            await ctx.send("You set {} as the coaching channel".format(channel))
        else:
            await ctx.send("This command only works in the Legend eSports server")


    @commands.guild_only()
    @coaching.command()
    async def status(self, ctx, member: discord.Member):
        """Shows information regarding a particular player"""
        if ctx.guild.id == 445092370006933505:
            data = self.config.guild(ctx.guild)
            lst = await data.get_raw('neededlist')
            coach = await data.coachid()
            coach_role = ctx.guild.get_role(coach)
            x = ctx.author.roles
            x.pop(0)
            for roles in x:
                if roles.position >= coach_role.position:
                    if member.id in lst:
                        player_data = self.config.member(member)
                        ign_use = await player_data.get_raw('ign')
                        tag_use = await player_data.get_raw('tag')
                        time_use = await player_data.get_raw('time')
                        deck_use = await player_data.get_raw('deck_type')
                        await self.emb(ctx, "Discord Name", "In Game Name", "Player Tag", "Preferred Time", "Deck Type",
                                       member.mention, ign_use, tag_use, time_use, deck_use)
                        break

                    else:
                        await ctx.send("The member has not registered for coaching")
                        break
                else:
                    await ctx.send("You are not allowed to do that")
                    break
        else:
            await ctx.send("This command only works in the Legend eSports server")



