import cassiopeia as cass
from cassiopeia import Summoner, Queue
from datapipelines.common import NotFoundError
import discord
from discord.commands import (
    slash_command,
)
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command()
    async def player(self, ctx, name, region='NA'):
        summoner = Summoner(name=name, region=region)
        if (summoner.exists != True): 
                embed = discord.Embed(title=f"{name}",
                            description=f"{name} does not exist.")
                icon_url="https://ddragon.leagueoflegends.com/cdn/12.4.1/img/profileicon/0.png"
        else:
            try:
                cms = cass.get_champion_masteries(summoner, region)
                icon_url = summoner.profile_icon.url
                embed = discord.Embed(title=f"{summoner.name}",
                    description=f"""Level: {summoner.level}
Rank: {summoner.ranks[Queue.ranked_solo_fives]}
Top Champ: {cms[0].champion.name} Level: {cms[0].level}
Second: {cms[1].champion.name} Level: {cms[1].level}
Third: {cms[2].champion.name} Level: {cms[2].level}"""
                    , color=0xFFFFFF)

            except KeyError:
                embed = discord.Embed(title=f"{summoner.name}",
                        description=f"""Level: {summoner.level}
Rank: Unranked
Top Champ: {cms[0].champion.name} Level: {cms[0].level}
Second: {cms[1].champion.name} Level: {cms[1].level}
Third: {cms[2].champion.name} Level: {cms[2].level}"""
                        , color=0xFFFFFF)
        embed.set_thumbnail(url=icon_url)
        await ctx.respond(embed=embed)
        
    # x = summoner.current_match.participants[0].side
    # print(x)
    #I need to sort this somehow, but I'm not sure how, and Match v5 is broken so this is not gonna happen for now
    @slash_command()
    async def game(self, ctx, name, region='NA'):
        summoner = Summoner(name=name, region=region)
        try: 
            game = summoner.current_match
            x = game.participants.by_team
            print(x)
            embed = discord.Embed(title=f"{summoner.name}'s game",
                              description="Place Holder",
                              color=0xFFFFFF)  
        except NotFoundError:
            embed = discord.Embed(title=f"{summoner.name}'s game",
                              description=f"{summoner.name} is currently not in a gamep",
                              color=0xFFFFFF)
        embed.set_thumbnail(url=summoner.profile_icon.url)
        await ctx.respond(embed=embed)