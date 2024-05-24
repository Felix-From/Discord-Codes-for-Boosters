import json
class Config:
    def __init__(self) -> None:
        self.BOT_TOKEN = "xxxxxxxxxxxxxxxxx" # Bot Token from Discord Dev Board
        self.MAIN_CAT_ID = 1000000000000000000 # Category ID (for the User Channels)
        self.SERVER_ID = 1000000000000000000 # Server/Guild ID for the Server to interact.
        self.LOG_CHANNEL_ID = 1000000000000000000 # ChannelID for the Log Channel
        self.MESSAGE_CHANNEL_ID = 1000000000000000000 # ChannelID for the ReactionUI element (The Channel where ppl request a code)
        self.ERROR_CHANNEL_ID = 1000000000000000000 # ChannelID for ERROR Msg !! Currently UNUSED!!
        self.ROLE_TO_INTERACT = [
            1000000000000000000
        ] # Role you need to Interact with the Bot -> should be set to the Booster Role ID
        self.BOT_CONTROL_ROLES = [
            1000000000000000000
        ] # Roles that can use the Debug commands, and those Roles will be able to see UserCodeChannels
        self.BOT_NAME = "Bot McBotting" # Name of the Bot
        self.BOT_PREFIX = "!" # OldScool Command Prefix !! Currently UNUSED !!
        self.BOT_DESCRIPTION = "I'm a Bot!" # Description of the Bot
        self.BOT_ACTIVITY = "with some Booster-Codes" #Bot is playing XYZ
        self.BOT_FOOTERTEXT = "Boost your Game!"# End of Embeds
        self.BOT_ICONLINK = "https://link.to/your/img/"# Icon for Embeds footers
        ## Mysql
        self.MYSQL_HOST = "Database_IP"
        self.MYSQL_USER = "NotRoot"
        self.MYSQL_PASSWORD = "NotRootPassword"
        self.MYSQL_DATABASE = "Database_name"
        ## Rates (Randomroll(1,10000)*Rate == Same RandomRoll)
        self.CodeContentChance_UNCOMMON=0.2 # like 20%
        self.CodeContentChance_RARE=0.1 # like 10%
        self.CodeContentChance_EPIC=0.05 # like 5%
        self.CodeContentChance_LEGENDARY=0.01 #like 1%
        self.CodeContentChance_RNGESUS=0.0001 #like 0,01%
        pass

with open("bot_config.json", "w") as f:
    json.dump(Config().__dict__, f, indent=4)
    print("done")

