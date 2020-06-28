from redbot.core import Config, commands, checks
import discord


class esports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=53565445636546)
        default_guild = {'academy': None,
                         'challenger': None,
                         'mainteam': None,
                         'tryoutmanager': None,
                         'tryout': None,
                         'academyscrimid': None,
                         'challengerscrimid': None}

        self.config.register_guild(**default_guild)

    @commands.guild_only()
    @commands.command()
    async def approveteam(self, ctx, team_name, user: discord.Member):
        """Approves a user for a team role"""
        if ctx.guild.id == 445092370006933505:
            data = self.config.guild(ctx.guild)

            academyid = await data.academy()
            academyrole = ctx.guild.get_role(academyid)

            challengerid = await data.challenger()
            challengerrole = ctx.guild.get_role(challengerid)

            mainid = await data.mainteam()
            mainrole = ctx.guild.get_role(mainid)

            tryoutmanid = await data.tryoutmanager()
            tryoutmanrole = ctx.guild.get_role(tryoutmanid)

            tryoutid = await data.tryout()
            tryoutrole = ctx.guild.get_role(tryoutid)

            team_name = team_name.lower()

            author_role = ctx.author.top_role

            if tryoutmanid is None or tryoutid is None or mainid is None or academyid is None or challengerid is None:
                await ctx.send("Roles have not been set correctly")

            elif author_role >= tryoutmanrole:
                if team_name == "academy" and academyid is not None:
                    await user.add_roles(academyrole)
                    await user.remove_roles(tryoutrole)
                    await ctx.send("Academy roles added and tryout roles removed")
                elif team_name == "challenger" and challengerid is not None:
                    await user.add_roles(challengerrole)
                    await user.remove_roles(tryoutrole)
                    await ctx.send("Challenger roles added and tryout roles removed")
                elif team_name == "main" and mainid is not None:
                    await user.add_roles(mainrole)
                    await user.remove_roles(tryoutrole)
                    await ctx.send("Main team role added and tryout roles removed")
                else:
                    await ctx.send("Incorrect team name please choose a team name from Academy, Challenger, Main")
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
    async def challengerscrimrole(self, ctx, *, users: str):
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
    async def challengerscrim(self, ctx):
        if ctx.guild.id == 445092370006933505:

            cscrimid = await self.config.guild(ctx.guild).academyscrimid()
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
    async def setchallengerrole(self, ctx, role: discord.Role):
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
    async def settryoutrole(self, ctx, role: discord.Role):
        """Sets the required roles role"""
        if ctx.guild.id == 445092370006933505:
            id = role.id
            await self.config.guild(ctx.guild).tryout.set(int(id))
            await ctx.send("You set {} as the tryout role id".format(role.id))
        else:
            pass

    @checks.mod_or_permissions()
    @commands.guild_only()
    @commands.command()
    async def setchallengerscrimrole(self, ctx, role: discord.Role):
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
