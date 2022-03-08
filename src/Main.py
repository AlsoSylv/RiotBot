import cassiopeia as cass
import discord
from cassiopeia import Summoner
from commands.Stats import Stats
from commands import ConfigFile, cdragonrates

def setup(bot):
    bot.add_cog(Stats(bot))

config = ConfigFile.Config

#Test call to make sure that everything is working
cass.set_riot_api_key(config.APIKey)

summoner = Summoner(name="NewClownPrince", region="NA")
print("Test {name} {level} {region} {icon}".format(name=summoner.name,
                                            level=summoner.level,
                                            region=summoner.region,
                                            icon=summoner.profile_icon.url,))

cdragonrates
bot = discord.Bot()

setup(bot)
bot.run(config.BotKey)