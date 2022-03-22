import cassiopeia as cass
import discord, re, requests, time
from cassiopeia import Summoner, Queue
from datapipelines.common import NotFoundError
from discord.ext import commands
from roleidentification import pull_data
from cassiopeia.core import champion
from roleidentification.utilities import get_team_roles
from LoL_Scrapper import ugg

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
                icon_url="https://ddragon.leagueoflegends.com/cdn/12.5.1/img/profileicon/0.png"
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
        
    @slash_command()
    async def game(self, ctx, name, region='NA'):
        await ctx.defer()
        summoner = Summoner(name=name, region=region)
        if (summoner.exists != True):
            embed = discord.Embed(title=f"{name}",
                            description=f"{name} does not exist.")
            icon_url="https://ddragon.leagueoflegends.com/cdn/12.5.1/img/profileicon/0.png"
            embed.set_thumbnail(url=icon_url)
            await ctx.respond(embed=embed)
        else:
            try: 
                game = cass.get_current_match(summoner, region)
                champion_roles = pull_data()
                
                blue_team = [1, 2, 3, 4, 5]
                Blue_champs = [1, 2, 3, 4, 5]
                Blue_ranks = [1, 2, 3, 4, 5]
                
                Blue = game.blue_team
                Blue_player = Blue.participants
                Blue_roles = get_team_roles(Blue, champion_roles)
                
                red_team = [1, 2, 3, 4, 5]
                Red_champs = [1, 2, 3, 4, 5]
                Red_ranks = [1, 2, 3, 4, 5]
                
                Red = game.red_team
                Red_player = Red.participants
                Red_roles = get_team_roles(Red, champion_roles)
                
                Blue_id = [1, 2, 3, 4, 5]
                Red_id = [1, 2, 3, 4, 5]
                
                blue_roles = [champion.id for roles, champion in Blue_roles.items()]
                red_roles = [champion.id for roles, champion in Red_roles.items()]
                for y in range(5):               
                    for ii, i in enumerate(blue_roles):
                        if i == Blue_player[y].champion.id:
                            blue_team[ii] = Blue_player[y].summoner.name
                            Blue_champs[ii] =  Blue_player[y].champion.name
                            Blue_id[ii] = Blue_player[y].champion.id
                            try:
                                Blue_ranks[ii] = Blue_player[y].summoner.ranks[Queue.ranked_solo_fives]
                            except:
                                Blue_ranks[ii] = 'Unranked'
                print(blue_roles)
                print(Blue_id)
                
                for y in range(5):
                    for ii, i in enumerate(red_roles):
                        if i == Red_player[y].champion.id:
                            red_team[ii] = Red_player[y].summoner.sanitized_name
                            Red_champs[ii] = Red_player[y].champion.name
                            Red_id[ii] = Red_player[y].champion.id
                            try:
                                Red_ranks[ii] = Red_player[y].summoner.ranks[Queue.ranked_solo_fives]
                            except: 
                                Red_ranks[ii] = 'Unranked'
                print(Red_id)
                print(red_roles)
                
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
                              description=f"{summoner.name} is currently not in a game",
                              color=0xFFFFFF)
                icon_url=summoner.profile_icon.url
                embed.set_thumbnail(url=icon_url)
                await ctx.respond(embed=embed)
                
    @slash_command()
    async def uggstats(self, ctx, name, lane, region='NA'):
        await ctx.defer()
        u = ugg.UGG
        champ = re.sub(r'\W+', '', name.lower())
        try:
            wr = await u.Win_rate(champ, lane)
            br = await u.Ban_rate(champ, lane)
            pr = await u.Pick_rate(champ, lane)
            stats = await u.Shards(champ, lane)
            runes = await u.Runes(champ, lane)
            r = requests.get(f"https://raw.communitydragon.org/latest/game/assets/characters/{champ}/hud/{champ}_square.png")
            if r.status_code == 404:
                icon_url = f"https://raw.communitydragon.org/latest/game/assets/characters/{champ}/hud/{champ}_square_0.png"
            else:
                icon_url = f"https://raw.communitydragon.org/latest/game/assets/characters/{champ}/hud/{champ}_square.png"
            embed = discord.Embed(title=f"{name}", description=f"""Win rate: **{wr}**
Ban rate: **{br}**
Pick rate: **{pr}**
Primary: **{runes[0]}, {runes[1]}, {runes[2]}, {runes[3]}**
Secondary: **{runes[4]}, {runes[5]}**
Stats: **{stats[0]}, {stats[1]}, {stats[2]}**""", color=0xFFFFFF)
            embed.set_thumbnail(url=icon_url)
            await ctx.respond(embed=embed)
        except:
            icon_url = "https://raw.communitydragon.org/latest/game/data/images/ui/pingmia.png"
            embed = discord.Embed(title=f"{name}", description="Name or lane are misspelled", color=0xFFFFFF)
            embed.set_thumbnail(url=icon_url)
            await ctx.respond(embed=embed)