from redbot.core import Config, commands, checks
import discord
import clashroyale

class esports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.config = Config.get_conf(self, identifier=53565445636546)
        default_guild = {'academy': None,
                         'challenger': None,
                         'mainteam': None,
                         'tryoutmanager': None,
                         'academyscrimid': None,
                         'challengerscrimid': None}

        self.config.register_guild(**default_guild)
        self.abc = bot.get_cog("LegendEsports")
    async def crtoken(self):
        # Clash Royale API
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Use !set api clashroyale token,YOUR_TOKEN to set it")
        self.cr = clashroyale.official_api.Client(token=token['token'],
                                                  is_async=True,
                                                  url="https://proxy.royaleapi.dev/v1")

    @commands.guild_only()
    @commands.command()
    async def approveteam(self, ctx, team_name, user: discord.Member):
        """Approves a user for a team role"""
        if ctx.guild.id == 445092370006933505 or ctx.guild.id == 691577465797345300:

            LMT = self.bot.get_guild(740567594381213727)

            if user in LMT.members:
                await LMT.kick(user)

            data = self.config.guild(ctx.guild)

            player_tag = self.tags.getTag(userID = user.id)
            if player_tag is None:
                return await ctx.send("No tag saved, use the command `!save <your tage here>`")

            try:
                player_data = await self.cr.get_player(player_tag)
            except clashroyale.RequestError:
                return await ctx.send("Can't reach the supercell servers at the moment")

            ign = player_data.name

            academyid = await data.academy()
            academyrole = ctx.guild.get_role(academyid)

            challengerid = await data.challenger()
            challengerrole = ctx.guild.get_role(challengerid)

            mainid = await data.mainteam()
            mainrole = ctx.guild.get_role(mainid)

            tryoutmanid = await data.tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)

            academytryoutid = await self.abc.config.guild(ctx.guild).Academyt()
            academytryoutrole = ctx.guild.get_role(academytryoutid)

            challengertryoutid = await self.abc.config.guild(ctx.guild).Challengert()
            challengertryoutrole = ctx.guild.get_role(challengertryoutid)

            team_name = team_name.lower()

            author_role = ctx.author.top_role


            if tryoutmanid is None or academytryoutid is None or mainid is None or academyid is None or challengerid is None:
                await ctx.send("Roles have not been set correctly")

            elif author_role >= tryoutmanrole:
                if team_name == "academy" and academyid is not None:
                    await user.add_roles(academyrole)
                    await user.remove_roles(academytryoutrole)
                    await ctx.send("Academy roles added and tryout roles removed")
                    try:
                        final_name = "Academy | " + ign
                        await user.edit(nick=final_name)
                    except discord.HTTPException:
                        return await ctx.send("Not enough permissions but roles have been added")
                elif team_name == "main" or team_name == "main team" and challengerid is not None: # CHALLENGER REFERS TO MAIN 
                    await user.add_roles(challengerrole)
                    await user.remove_roles(challengertryoutrole)
                    try:
                        final_name = "Main Team | " + ign
                        await user.edit(nick=final_name)
                    except discord.HTTPException:
                        return await ctx.send("Not enough permissions but roles have been added")
                    await ctx.send("Main team roles added and tryout roles removed")
                elif (team_name == "pro" or team_name == "proteam") and mainid is not None: # MAIN TEAM REFERS TO PRO HERE
                    await user.add_roles(mainrole)
                    try:
                        final_name = "Pro | " + ign
                        await user.edit(nick=final_name)
                    except discord.HTTPException:
                        return await ctx.send("Not enough permissions to edit user name, but roles have been added")
                    await ctx.send("Pro team role added and tryout roles removed")
                else:
                    await ctx.send("Incorrect team name please choose a team name from Academy, Main, Pro")
            else:
                await ctx.send("You do not have permissions to do that")
        else:
            pass

    @commands.guild_only()
    @commands.command()
    async def academyscrimrole(self, ctx, *, users: str):
        if ctx.guild.id == 445092370006933505:
            ascrimid = await self.config.guild(ctx.guild).academyscrimid()
            academyscrimrole = ctx.guild.get_role(ascrimid)

            tryoutmanid = await self.config.guild(ctx.guild).tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)
            users = users.split()

            if ctx.author.top_role >= tryoutmanrole:
                for user in users:
                    userid = user.strip('<@!>')
                    new_user = ctx.guild.get_member(user_id=int(userid))
                    await new_user.add_roles(academyscrimrole)
                await ctx.send("Roles have been added")

            else:
                await ctx.send("You don't have enough permissions to execute this command")
        else:
            pass

    @commands.guild_only()
    @commands.command()
    async def mainscrimrole(self, ctx, *, users: str):
        if ctx.guild.id == 445092370006933505:

            cscrimid = await self.config.guild(ctx.guild).challengerscrimid()
            challengerscrimrole = ctx.guild.get_role(cscrimid)

            tryoutmanid = await self.config.guild(ctx.guild).tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)
            users = users.split()

            if ctx.author.top_role >= tryoutmanrole:
                for user in users:
                    userid = user.strip('<@!>')
                    new_user = ctx.guild.get_member(user_id=int(userid))
                    await new_user.add_roles(challengerscrimrole)
                await ctx.send("Roles have been added")
            else:
                await ctx.send("You don't have enough permissions to execute this command")
        else:
            pass

    @commands.guild_only()
    @commands.group()
    async def reset(self, ctx):
        """Resets the roles"""

    @commands.guild_only()
    @reset.command()
    async def academyscrim(self, ctx):
        if ctx.guild.id == 445092370006933505:

            ascrimid = await self.config.guild(ctx.guild).academyscrimid()
            academyscrimrole = ctx.guild.get_role(ascrimid)

            tryoutmanid = await self.config.guild(ctx.guild).tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)

            members = academyscrimrole.members
            if ctx.author.top_role >= tryoutmanrole:
                for member in members:
                    await member.remove_roles(academyscrimrole)
                await ctx.send("Done!")
            else:
                await ctx.send("You do not have the permissions to do that")
        else:
            pass

    @commands.guild_only()
    @reset.command()
    async def mainscrim(self, ctx):
        if ctx.guild.id == 445092370006933505:

            cscrimid = await self.config.guild(ctx.guild).challengerscrimid()
            challengerscrimrole = ctx.guild.get_role(cscrimid)

            tryoutmanid = await self.config.guild(ctx.guild).tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)

            members = challengerscrimrole.members
            if ctx.author.top_role >= tryoutmanrole:
                for member in members:
                    await member.remove_roles(challengerscrimrole)
                await ctx.send("Done!")
            else:
                await ctx.send("You do not have the permissions to do that")
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setacademyrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).academy.set(int(id))
            await ctx.send("You set {} as the academy role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setmainteamrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).challenger.set(int(id))
            await ctx.send("You set {} as the challenger role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setmainteamrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).mainteam.set(int(id))
            await ctx.send("You set {} as the main team role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def settryoutmanagerrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).tryoutmanager.set(int(id))
            await ctx.send("You set {} as the tryoutmanager role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setmainscrimrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).challengerscrimid.set(int(id))
            await ctx.send("You set {} as the challenger scrim role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setacademyscrimrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).academyscrimid.set(int(id))
            await ctx.send("You set {} as the academy scrim role id".format(role.id))
        else:
            pass
