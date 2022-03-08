import cassiopeia as cass
import discord
from cassiopeia import Summoner, Queue
from datapipelines.common import NotFoundError
from discord.ext import commands
from roleidentification import pull_data
from cassiopeia.core import champion
from roleidentification.utilities import get_team_roles
from discord.commands import (
    slash_command,
)

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command()
    async def player(self, ctx, name, region='NA'):
        summoner = Summoner(name=name, region=region)
        if (summoner.exists != True): 
                embed = discord.Embed(title=f"{name}",
                            description=f"{name} does not exist.")
                icon_url="https://ddragon.leagueoflegends.com/cdn/latest/img/profileicon/0.png"
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

            except:
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
        await ctx.defer()
        summoner = Summoner(name=name, region=region)
        if (summoner.exists != True):
            embed = discord.Embed(title=f"{name}",
                            description=f"{name} does not exist.")
            icon_url="https://ddragon.leagueoflegends.com/cdn/latest/img/profileicon/0.png"
            embed.set_thumbnail(url=icon_url)
            await ctx.respond(embed=embed)
        else:
            try: 
                game = cass.get_current_match(summoner, region)
                champion_roles = pull_data()
                blue_team = []
                Blue_champs = []
                Blue_ranks = []
                Blue = game.blue_team
                Blue_player = Blue.participants
                Blue_roles = get_team_roles(Blue, champion_roles)
                red_team = []
                Red_champs = []
                Red_ranks = []
                Red = game.red_team
                Red_player = Red.participants
                Red_roles = get_team_roles(Red, champion_roles)
#            print({role.name: champion.id for role, champion in Blue_roles.items()})
                blue_roles = [champion.id for roles, champion in Blue_roles.items()]
                red_roles = [champion.id for roles, champion in Red_roles.items()]
#            print(blue_roles)
                #Blue Team
                for y in range(5):
                    if Blue_player[y].champion.id == blue_roles[0]:
                        blue_team.insert(0, Blue_player[y].summoner.name)
                        Blue_champs.insert(0, Blue_player[y].champion.name)
                        try:
                            Blue_ranks.insert(0, Blue_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Blue_ranks.insert(0, 'Unranked')
                    elif Blue_player[y].champion.id == blue_roles[1]:
                        blue_team.insert(1, Blue_player[y].summoner.name)
                        Blue_champs.insert(1, Blue_player[y].champion.name)
                        try:
                            Blue_ranks.insert(1, Blue_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Blue_ranks.insert(1, 'Unranked')
                    elif Blue_player[y].champion.id == blue_roles[2]:
                        blue_team.insert(2, Blue_player[y].summoner.name)
                        Blue_champs.insert(2, Blue_player[y].champion.name)
                        try:
                            Blue_ranks.insert(2, Blue_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Blue_ranks.insert(2, 'Unranked')
                    elif Blue_player[y].champion.id == blue_roles[3]:
                        blue_team.insert(3, Blue_player[y].summoner.name)
                        Blue_champs.insert(3, Blue_player[y].champion.name)
                        try:
                            Blue_ranks.insert(3, Blue_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Blue_ranks.insert(3, 'Unranked')
                    else: # Blue_player[y].champion.id == blue_roles[4]
                        blue_team.insert(4, Blue_player[y].summoner.name)
                        Blue_champs.insert(4, Blue_player[y].champion.name)
                        try:
                            Blue_ranks.insert(4, Blue_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Blue_ranks.insert(4, 'Unranked')
                print(blue_team)
                
                #Red Team
                for y in range(5):
                    if Red_player[y].champion.id == red_roles[0]:
                        red_team.insert(0, Red_player[y].summoner.name)
                        Red_champs.insert(0, Red_player[y].champion.name)
                        try:
                            Red_ranks.insert(0, Red_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Red_ranks.insert(0, 'Unranked')
                    elif Red_player[y].champion.id == red_roles[1]:
                        red_team.insert(1, Red_player[y].summoner.name)
                        Red_champs.insert(1, Red_player[y].champion.name)
                        try:
                            Red_ranks.insert(1, Red_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Red_ranks.insert(1, 'Unranked')
                    elif Red_player[y].champion.id == red_roles[2]:
                        red_team.insert(2, Red_player[y].summoner.name)
                        Red_champs.insert(2, Red_player[y].champion.name)
                        try:
                            Red_ranks.insert(2, Red_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Red_ranks.insert(2, 'Unranked')
                    elif Red_player[y].champion.id == red_roles[3]:
                        red_team.insert(3, Red_player[y].summoner.name)
                        Red_champs.insert(3, Red_player[y].champion.name)
                        try:
                            Red_ranks.insert(3, Red_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Red_ranks.insert(3, 'Unranked')
                    else: # Red_player[y].champion.id == red_roles[4]
                        red_team.insert(4, Red_player[y].summoner.name)
                        Red_champs.insert(4, Red_player[y].champion.name)
                        try:
                            Red_ranks.insert(4, Red_player[y].summoner.ranks[Queue.ranked_solo_fives])
                        except:
                            Red_ranks.insert(4, 'Unranked')
                print(red_team)
                
                embed = discord.Embed(title=f"{summoner.name}'s game",
                              description=f"""Blue Team:
{blue_team[0]}, {Blue_ranks[0]}: playing {Blue_champs[0]}
{blue_team[1]}, {Blue_ranks[1]}: playing {Blue_champs[1]}
{blue_team[2]}, {Blue_ranks[2]}: playing {Blue_champs[2]}
{blue_team[3]}, {Blue_ranks[3]}: playing {Blue_champs[3]}
{blue_team[4]}, {Blue_ranks[4]}: playing {Blue_champs[4]}

Red Team:
{red_team[0]}, {Red_ranks[0]}: playing {Red_champs[0]}
{red_team[1]}, {Red_ranks[1]}: playing {Red_champs[1]}
{red_team[2]}, {Red_ranks[2]}: playing {Red_champs[2]}
{red_team[3]}, {Red_ranks[3]}: playing {Red_champs[3]}
{red_team[4]}, {Red_ranks[4]}: playing {Red_champs[4]}""",
                              color=0xFFFFFF)
                icon_url=summoner.profile_icon.url
                embed.set_thumbnail(url=icon_url)
                await ctx.respond(embed=embed)
            except NotFoundError:
                embed = discord.Embed(title=f"{summoner.name}'s game",
                              description=f"{summoner.name} is currently not in a gamep",
                              color=0xFFFFFF)
                icon_url=summoner.profile_icon.url
                embed.set_thumbnail(url=icon_url)
                await ctx.respond(embed=embed)
 
#This is not needed, cass always returns blue team then red team        
#            blue_team = []
#            red_team = []
#            y = 0
#            for y in range(10):
#                if game.participants[y].side is Side.blue:
#                    summonerBlue = game.participants[y]
#                    blue_team.append(summonerBlue.summoner.name)
#                    blue_team.append(summonerBlue.champion.name)
#                else:
#                    summonerRed = game.participants[y]
#                    red_team.append(summonerRed.summoner.name)
#                    red_team.append(summonerRed.champion.name)
#                print(blue_team)
#                print(red_team)