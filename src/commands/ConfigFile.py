import configparser

#This Config is read only, so there shouldn't be an issue?
class Config:
    def __init__(self, config):
        self.config = config 
        
    configFile = "config.toml"
    
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'RiotAPIKey' : '',
                         'DiscordBotKey' : ''}
    try:
        with open(configFile, 'x') as Configfile:
            config.write(Configfile)
    except FileExistsError:
        config.sections()
        config.read("config.toml")
    
        APIKey = config['DEFAULT']['RiotAPIKey']
        BotKey = config['DEFAULT']['DiscordBotKey']