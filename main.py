import mysql.connector
import nextcord
import nextcord.abc
from nextcord.ext import commands, menus
import json
import datetime
import mysql.connector
import random
import hashlib
import nextcord.types
import locale
import logging


## ------------------------------------------------
#LOAD Config from bot_config.json
## ------------------------------------------------

with open('bot_config.json', 'r') as f:
    config = json.load(f)

if config == None:
    print("Config file not found")
    exit()

## ------------------------------------------------
#LOAD content from content_config.json
## ------------------------------------------------

with open('content_config.json', 'r') as f:
    content_table = json.load(f)

if content_table == None:
    print("Content_config file not found")
    exit()

## ------------------------------------------------
#LOADED - CONST
## ------------------------------------------------

#Bot Init Config.
BOT_TOKEN = config.get("BOT_TOKEN")
MAIN_CAT_ID = config.get('MAIN_CAT_ID')
SERVER_ID = config.get('SERVER_ID')

#Roles who can use Admin stuff
BOT_CONTROL_ROLES = config.get('BOT_CONTROL_ROLES')

#Roles who can React to the Bot. (Get Code)
ROLE_TO_INTERACT = config.get('ROLE_TO_INTERACT')

#Bot Configs
BOT_NAME = config.get('BOT_NAME')
BOT_PREFIX = config.get('BOT_PREFIX')
BOT_DESCRIPTION = config.get('BOT_DESCRIPTION')
BOT_ACTIVITY = config.get('BOT_ACTIVITY')

#Bot Response Styles
BOT_FOOTERTEXT = config.get('BOT_FOOTERTEXT')
BOT_ICONLINK = config.get('BOT_ICONLINK')

#Bot Channels
MESSAGE_CHANNEL_ID = config.get('MESSAGE_CHANNEL_ID')
LOG_CHANNEL_ID = config.get('LOG_CHANNEL_ID')
ERROR_CHANNEL_ID = config.get('ERROR_CHANNEL_ID')

## ------------------------------------------------
#CONST - MYSQL
## ------------------------------------------------

MYSQL_HOST = config.get('MYSQL_HOST')
MYSQL_USER = config.get('MYSQL_USER')
MYSQL_PASSWORD = config.get('MYSQL_PASSWORD')
MYSQL_DATABASE = config.get('MYSQL_DATABASE')

##-------------------------------------------------
# Content Table Rates
##-------------------------------------------------

CODECHANCE_UNCOMMON = config.get('CodeContentChance_UNCOMMON')
CODECHANCE_RARE = config.get('CodeContentChance_RARE')
CODECHANCE_EPIC = config.get('CodeContentChance_EPIC')
CODECHANCE_LEGENDARY = config.get('CodeContentChance_LEGENDARY')
CODECHANCE_RNGESUS = config.get('CodeContentChance_RNGESUS')

## ------------------------------------------------
#STATIC - CONST
## ------------------------------------------------

BOT_EMBED_COLOR = nextcord.Color.teal()

## ------------------------------------------------
#Vars
## ------------------------------------------------

locale.setlocale(locale.LC_TIME,"de_DE")

## ------------------------------------------------
# Logging
## ------------------------------------------------
# Setup logger
logger = logging.getLogger('nextcord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

## ------------------------------------------------
#Classes
## ------------------------------------------------

class CodeChannels():
    """
    Represents a user's private channel in the server.

    Attributes:
        channel (nextcord.TextChannel): The private channel associated with the user.
        owner (nextcord.Member): The user who owns the private channel.
    """
    def __init__(self, channel : nextcord.TextChannel, owner : nextcord.Member):
        self.channel: nextcord.TextChannel = channel
        self.owner: nextcord.Member = owner

class ButtonReactMenu(menus.ButtonMenu):
    """
    A button-based menu for interacting with the bot.

    Attributes:
        None
    """
    async def send_initial_message(self, ctx, channel):
        """
        Sends the initial message for the menu.

        Parameters:
            ctx: The context in which the menu is being triggered.
            channel: The channel where the menu message will be sent.

        Returns:
            None
        """
        Bot_Creator = await bot.fetch_user(323828775584268288)
        Msg_Content = f"""
        Sie haben [CelestialV](https://discord.gg/celestialv) geboostet?
        Holen Sie sich noch heute einen Booster-Code!
        In Booster-Codes können eine Vielzahl von Preisen stecken!
        Von Geld über Items bis hin zu Auto's, die Liste ist lang!
        
        Drücken Sie auf "Code anfordern" um Ihren Code zu erhalten.
        Mit "Zeit anfordern!" schreibt der Bot die Zeit bis zum nächsten Code!
        Bei Fragen bitte an das Adminteam oder im Notfall {Bot_Creator.mention}
        """
        embed = nextcord.embeds.Embed(title="Dein Boost zählt!",description=Msg_Content,color=BOT_EMBED_COLOR)
        embed.set_thumbnail(BOT_ICONLINK)
        embed.set_footer(text = f"Boost your Game! - {str(datetime.datetime.now().strftime('%A %d.%m.%y, %H:%M Uhr'))}")
        await channel.send(embed=embed,view=self)
        self.result=True

    @nextcord.ui.button(label="Code anfordern!",style=nextcord.ButtonStyle.success)
    async def on_code_request(self, button, interaction:nextcord.interactions.Interaction):
        global sql_con,sql_cursor
        """
        Event handler for the "thumbs up" button interaction.

        Parameters:
            button: The button that was clicked.
            interaction (nextcord.interactions.Interaction): The interaction triggered by the button click.

        Returns:
            None
        """
        sql_con.reconnect()
        sql_cursor = sql_con.cursor()
        for role in ROLE_TO_INTERACT:
            if role in interaction.user._roles:
                await interaction.response.defer()
                interaction.response.is_done()
                await handle_Code_Request(interaction)
                return
        await interaction.response.send_message("Du bist kein Booster!",ephemeral=True)
        return

    @nextcord.ui.button(label="Zeit anfordern!",style=nextcord.ButtonStyle.blurple)
    async def on_time_request(self, button, interaction:nextcord.interactions.Interaction):
        global sql_con,sql_cursor
        sql_con.reconnect() #Reconnect Mysql.
        sql_cursor = sql_con.cursor()
        time = await check_time_for_new_code(interaction.user)# Get Timestamp of last Code Log Entry
        if time == None or time == False: # Check if User has a Code Log Entry
            await interaction.response.send_message("Du hast noch keinen Code!",ephemeral=True) #Send Response
            return
        time_last = time[0] 
        time_new = time[1]
        content = f"""
        Du hast dein letzten Code am {time_last.strftime('%A %d.%m.%y um %H:%M Uhr')} abgeholt!\nDein nächsten Code kannst du am {time_new.strftime('%A %d.%m.%y um %H:%M Uhr')} abholen!
        """
        await interaction.response.send_message(content=content,ephemeral=True) # Send Response
        return

    # @nextcord.ui.button(emoji="\N{BLACK SQUARE FOR STOP}\ufe0f")
    # async def on_stop(self, button, interaction):
    #     self.stop()

## ------------------------------------------------
# Bot Init
## ------------------------------------------------

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, description=BOT_DESCRIPTION)

list_CodeChannels : list[CodeChannels] = []

## ------------------------------------------------
# Main
## ------------------------------------------------

def main():
    """
    The main function to initialize and run the bot.
    """
    global sql_con,sql_cursor
    sql_con = connect_to_mysql(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DATABASE)# Connect to MYSQL
    if sql_con == None: # Bot beenden wenn es nicht geht.
        return quit() 
    sql_cursor = sql_con.cursor()
    bot.activity = nextcord.Activity(type=nextcord.ActivityType.playing, name=BOT_ACTIVITY) # Set bot Activity to Config
    bot.run(BOT_TOKEN) # Init BOT
## ------------------------------------------------
# Main Events
## ------------------------------------------------

@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready and connected.
    """
    print(f'We have logged in as {bot.user}')
    await __initUserChannels() #Load all UserChannel into a List
    server = bot.get_guild(SERVER_ID) #Gets the "main" Server
    msg_chnl = server.get_channel(MESSAGE_CHANNEL_ID) # Gets the MESSAGE_CHANNEL for init message.
    await msg_chnl.set_permissions(server.default_role,add_reactions = False) # removes "reaction" perms
    await msg_chnl.set_permissions(server.default_role,send_messages = False) # removes "send_message" perms
    await msg_chnl.set_permissions(server.me,send_messages=True) # Give "send_message" perm to BOT
    await server.me.edit(nick=BOT_NAME) # Change the Username to Config.
    messages = await msg_chnl.history(limit=200).flatten() # Clear old Messages
    for message in messages:
        if message.author.id == bot.user.id:
            await message.delete()
    btn = ButtonReactMenu(timeout=None) #Create Button Menu
    await btn.send_initial_message(server,msg_chnl) # Send it.

@bot.event
async def on_message(message: nextcord.Message):
    """
    Event handler for when a message is received.

    Parameters:
        message (nextcord.Message): The message object received.

    Returns:
        None
    """
    if message.author == bot.user:
        return
    
    if message.guild.id != SERVER_ID:
        return
    
    #for user in message.guild.premium_subscribers:
        #await message.channel.send("Server Booster: "+user.global_name+" | "+user.name+" | "+str(user.id))
    return

## ------------------------------------------------
# Commands
## ------------------------------------------------

@bot.slash_command(description="Initilize Bot", guild_ids=[SERVER_ID])
@commands.has_any_role(BOT_CONTROL_ROLES)
async def initilize_bot(interaction: nextcord.Interaction):
    """
    !!DEBUG!!
    Initializes the bot.

    Parameters:
        interaction (nextcord.Interaction): The interaction object triggered by the command.

    Returns:
        None
    """
    await ButtonReactMenu().start(interaction=interaction)
    return

@bot.slash_command(description="Erstelle [x] anzahl an Codes",guild_ids=[SERVER_ID])
@commands.has_any_role(BOT_CONTROL_ROLES)
async def create_codes(interaction: nextcord.Interaction, amount: int):
    """
    !!ADMIN COMMAND!!
    Creates a specified number of codes.

    Parameters:
        interaction (nextcord.Interaction): The interaction object triggered by the command.
        amount (int): The number of codes to be generated.

    Returns:
        None
    """
    if amount <=0:
        await interaction.response.send_message("Bitte gib eine Zahl größer 0 an!",ephemeral=True)
        return
    else:
        await interaction.response.defer(ephemeral=True,with_message=False)
        await __generate_Codes_admin(interaction.user,amount)
    return

@bot.slash_command(description="Reloads the Bots Contenttable", guild_ids=[SERVER_ID])
@commands.has_any_role(BOT_CONTROL_ROLES)
async def reload_content(interaction: nextcord.Interaction):
    """
    !!DEBUG!!
    Reloads the content table used by the bot.

    Parameters:
        interaction (nextcord.Interaction): The interaction object triggered by the command.

    Returns:
        None
    """
    __reload_Code_Content()
    return await interaction.response.send_message("Contenttable reloaded!",ephemeral=True)

@bot.slash_command(description="Tests the Bots Contenttable", guild_ids=[SERVER_ID])
@commands.has_any_role(BOT_CONTROL_ROLES)
async def test_content(interaction: nextcord.Interaction):
    """
    !!DEBUG!!
    Tests the content generation functionality of the bot.

    Parameters:
        interaction (nextcord.Interaction): The interaction object triggered by the command.

    Returns:
        None
    """
    await interaction.response.defer()
    content_type, content_data, content_rarity = await __generate_Conent_for_Code(5)
    embed,file = await __createEmbedForContent(content_type,content_data,"123123123123",content_rarity)
    return await interaction.followup.send("",ephemeral=True,embed=embed,file=file)

@bot.slash_command(description="Gibt dir einen TestCode", guild_ids=[SERVER_ID])
@commands.has_any_role(BOT_CONTROL_ROLES)
async def codetest(interaction: nextcord.Interaction):
    """
    !!DEBUG!!
    Provides a test code to the user.

    Parameters:
        interaction (nextcord.Interaction): The interaction object triggered by the command.

    Returns:
        None
    """
    channel = await createUserChannel(interaction.guild, interaction.user)
    await interaction.response.send_message("Gut! - Hier ist dein Code!")

## ------------------------------------------------
#Common Functions
## ------------------------------------------------

def get_Member(guild: nextcord.guild, id: int = None, name: str=None, global_name : str = None) -> nextcord.Member:
    """
    Finds a member in the guild based on various criteria.

    Parameters:
        guild (discord.Guild): The guild to search for the member in.
        id (int, optional): The ID of the member you're looking for.
        name (str, optional): The name of the member you're looking for.
        global_name (str, optional): The username (global name) of the member you're looking for.

    Returns:
        discord.Member: 
            - If a member is found matching the provided criteria, it returns that member.
            - If no member is found, it returns None.

    Note:
        - This function helps find a member by their ID, name, or global username (the name you see on their profile).
        - If you provide multiple criteria (like ID and name), it prioritizes them in the order they're listed in the parameters.
        - If it can't find a member that matches your criteria, it returns None.
    """
    for member in guild.members:
        if id is not None and member.id == id:
            return member
        if name is not None and member.name == name:
            return member
        if global_name is not None and member.global_name == name:
            return member
        return None
    
def get_role(guild: nextcord.Guild, id:int=None, name:str=None, ids:list[int]= None , names:list[str] = None) -> nextcord.Role:
    """
    Helps you find a role in a specific guild based on different information.

    Parameters:
        guild (nextcord.Guild): The server (guild) where you're looking for the role.
        id (int, optional): The unique ID number of the role you want to find.
        name (str, optional): The name of the role you want to find.
        ids (List[int], optional): A list of ID numbers of roles you're interested in.
        names (List[str], optional): A list of role names you're interested in.

    Returns:
        Union[nextcord.Role, List[nextcord.Role], None]: 
            - If it finds a single role that matches your criteria, it gives you that role.
            - If it finds multiple roles matching your criteria (using `ids` or `names`), it gives you a list of those roles.
            - If it can't find any roles that match your criteria, it tells you nothing.

    Note:
        - If you provide both `ids` and `names`, it looks for roles matching any of the IDs or names.
        - If you provide `ids` or `names`, and there are no matching roles, it gives you nothing.
    """
    roles = []
    for role in guild.roles:
        if id is not None and role.id == id:
            return role
        if name is not None and role.name == name:
            return role
        if ids is not None and role.id in ids:
            roles.append(role)
        if names is not None and role.name in names:
            roles.append(role)

    if ids is not None or names is not None:
        return roles
    return None
## ------------------------------------------------
## MYSQL Functions
## ------------------------------------------------

def connect_to_mysql(host, username, password, database):
    try:
        # Establish connection to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
        else:
            print("Failed at connecting to MySQL database")
            return None
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL database:", error)
        return None

## ------------------------------------------------
## Code Functions
## ------------------------------------------------

def __reload_Code_Content():
    global content_table
    with open('content_config.json', 'r') as f:
        content_table = json.load(f)
    if content_table == None:
        print("Content_config file not found")
        exit()

async def __generate_Conent_for_Code(overwrite = None):
    choosen = random.randint(1,10000)
    if choosen <= 10000*CODECHANCE_RNGESUS or overwrite ==5:
        content_rarity = "RNGESUS"
        content_list = content_table.get('RNGESUS')
    elif choosen <= 10000*CODECHANCE_LEGENDARY or overwrite ==4:
        content_rarity = "legendary"
        content_list = content_table.get('legendary')
    elif choosen <= 10000*CODECHANCE_EPIC or overwrite ==3:
        content_rarity = "epic"
        content_list = content_table.get('epic')
    elif choosen <= 10000*CODECHANCE_RARE or overwrite ==2:
        content_rarity = "rare"
        content_list = content_table.get('rare')
    elif choosen <= 10000*CODECHANCE_UNCOMMON or overwrite ==1:
        content_rarity = "uncommon"
        content_list = content_table.get('uncommon')
    else:
        content_rarity = "common"
        content_list = content_table.get('common') #Common

    choosen_content = random.choice(content_list)
    choosen_type = choosen_content["type"]
    return choosen_type,choosen_content, content_rarity

async def __generate_Codes_admin(User: nextcord.User ,Anzahl:int = 1):
    failed_count = 0
    for _ in range(0,Anzahl):
        rndInt = random.randint(10,25000)
        unhashed_code = str(int((rndInt * User.id) / 7))+User.name
        hashed_code = hashlib.md5(unhashed_code.encode('utf-8')).hexdigest()
        hashed_code = hashed_code[int(len(hashed_code)/2):]
        formatted_code = '-'.join([hashed_code[i:i+4] for i in range(0, len(hashed_code), 4)])
        content_type, content_data, content_rarity = await __generate_Conent_for_Code()
        content_data = json.dumps(content_data)
        #MYSQL Check if Code Already Exists if not insert it
        #INSERT INTO `code_data`(`code`, `type`, `content`, `created_at`, `created_from`)
        sql_cursor.execute(f"SELECT * FROM code_data WHERE code = '{formatted_code}'")
        if sql_cursor.fetchone() is not None:
            failed_count +=1
            continue
        sql_cursor.execute(f"INSERT INTO code_data (code,type,rarity,content,created_at,created_from) VALUES('{formatted_code}',{content_type},'{content_rarity}','{content_data}',NOW(),'{str(User.id)} via CodeBot.');")
        last_id = sql_cursor.lastrowid
        sql_con.commit()
        await log_msg(bot.get_guild(SERVER_ID),f"MANY CODE GENERATED | Code: {formatted_code} | Typ: {content_type} | Content : {content_data} | Code_ID {last_id} | Creator: {User.id} - {User.name}")
        #wait interaction.user.send(f"Dein Code lautet: {formatted_code}")
    if failed_count > 0:
        __generate_Codes_admin(User,failed_count)

async def __generate_Code(User: nextcord.User):
    failed_count = 0
    rndInt = random.randint(10,25000)
    unhashed_code = str(int((rndInt * User.id) / 7))+User.name
    hashed_code = hashlib.sha1(unhashed_code.encode('utf-8')).hexdigest()
    hashed_code = hashlib.md5(hashed_code.encode('utf-8')).hexdigest()
    hashed_code = hashed_code[int(len(hashed_code)/2):]
    formatted_code = '-'.join([hashed_code[i:i+4] for i in range(0, len(hashed_code), 4)])
    content_type, content_data, content_rarity = await __generate_Conent_for_Code()
    content_data = json.dumps(content_data)
    #MYSQL Check if Code Already Exists if not insert it
    #INSERT INTO `code_data`(`code`, `type`, `content`, `created_at`, `created_from`)
    sql_cursor.execute(f"SELECT * FROM code_data WHERE code = '{formatted_code}'")
    if sql_cursor.fetchone() is not None:
        failed_count +=1
    else:
        sql_cursor.execute(f"INSERT INTO code_data (code,type,rarity,content,created_at,created_from) VALUES('{formatted_code}',{content_type},'{content_rarity}','{content_data}',NOW(),'AUTOGEN via CodeBot | Triggered by {User.id} - {User.name}');")
        last_id = sql_cursor.lastrowid
        sql_con.commit()
        await log_msg(bot.get_guild(SERVER_ID),f"CODE GENERATED | Code: {formatted_code} | Typ: {content_type} | Content : {content_data} | Code_ID {last_id} | TriggeredBy: {User.id} - {User.name}")
        return last_id
    #wait interaction.user.send(f"Dein Code lautet: {formatted_code}")
    if failed_count > 0:
       return __generate_Codes_admin(User,failed_count)
        
async def __check_if_user_gets_Code(User: nextcord.User):
    sql_request = f"SELECT * FROM code_log WHERE discord_user_id = '{User.id}' AND time BETWEEN NOW() + INTERVAL -1 MONTH AND NOW()"
    #INSERT INTO `code_log`(`discord_user_id`, `discord_user_name`, `time`, `code_id`, `code`) VALUES ('323828775584268288','Coffmann',NOW(),'123','123456578')
    #Send Mysql Query and Recieving the result
    sql_cursor.execute(sql_request)
    result = sql_cursor.fetchone()
    if result is None:
        return True
    else:
        if len(result) > 0:
            #await User.send(result) #Debug
            return False
    return

async def check_time_for_new_code(User: nextcord.User):
    sql_request = f"SELECT time,time+ INTERVAL +1 MONTH as timenew FROM code_log WHERE discord_user_id = '{User.id}' AND time BETWEEN NOW() + INTERVAL -1 MONTH AND NOW()"
    #INSERT INTO `code_log`(`discord_user_id`, `discord_user_name`, `time`, `code_id`, `code`) VALUES ('323828775584268288','Coffmann',NOW(),'123','123456578')
    #Send Mysql Query and Recieving the result
    sql_cursor.execute(sql_request)
    result = sql_cursor.fetchone()
    if result is None:
        return False
    else:
        if len(result) > 0:
            return result
    return

async def handle_Code_Request(interaction: nextcord.interactions.Interaction):
    #Create or Select Existing Channel
    objectCodeChannel : CodeChannels = await createUserChannel(interaction.guild, interaction.user)

    if(not await __check_if_user_gets_Code(interaction.user)):
        await interaction.followup.send(f"Du hast diesen Monat schon ein Code bekommen!\nSchaue in {objectCodeChannel.channel.mention} um deine aktuellen Code zu sehen!",ephemeral=True)
        return
    
    #Refill Codes list with one more
    await __generate_Code(interaction.user)
    #Get Codes
    sql_cursor.execute(f"SELECT id,code,type,rarity,content FROM code_data WHERE is_given_to_LogID = 0")
    results = sql_cursor.fetchall()
    #Ranzomize Code
    CodeNr = random.randint(0,len(results)-1)
    Redeem_Code_id = results[CodeNr][0]
    Redeem_Code_code = results[CodeNr][1]
    Redeem_Code_type = results[CodeNr][2]
    Redeem_Code_rarity = results[CodeNr][3]
    Redeem_Code_content= json.loads(results[CodeNr][4])

    #Create Log(History) Entry

    sql_cursor.execute(f"INSERT INTO `code_log`(`discord_user_id`, `discord_user_name`, `time`, `code_id`, `code`) VALUES ('{interaction.user.id}','{interaction.user.name}',NOW(),'{Redeem_Code_id}','{Redeem_Code_code}')")
    code_log_id = sql_cursor.lastrowid
    sql_cursor.execute("UPDATE code_data SET is_given_to_LogID = "+str(code_log_id)+" WHERE id = "+str( Redeem_Code_id)+";")
    sql_con.commit()
    await log_msg(interaction.guild,f"CODE-REQUEST | User: {interaction.user.global_name} | UserID: {interaction.user.id} | CODE: {Redeem_Code_code} | CODE ID: {Redeem_Code_id} | LogID : {code_log_id}",)

    #await objectCodeChannel.channel.send(f"Guten Tag {interaction.user.mention}!\nHier dein BoosterCode:\n12345asdfg12345")

    #Delete old Messages in User Channel
    messages = await objectCodeChannel.channel.history().flatten()
    for message in messages:
        if message.author.id == bot.user.id:
            if message.created_at.date().today() == datetime.datetime.now().date().today():
                await message.delete()
        
    msg,file = await __createEmbedForContent(Redeem_Code_type,Redeem_Code_content,Redeem_Code_code,Redeem_Code_rarity)

    # msg = nextcord.embeds.Embed(title="Dein Booster-Code!",description="Bitte ingame einlösen\n"+str(Redeem_Code_content))
    # msg.add_field(name="BoosterCode",value=str(Redeem_Code_code),inline=False)
    # msg.set_image(BOT_ICONLINK)
    # msg.set_footer(text=BOT_FOOTERTEXT,icon_url=BOT_ICONLINK)

    #print(f"INSERT INTO `code_log`(`discord_user_id`, `discord_user_name`, `time`, `code_id`, `code`) VALUES ('{interaction.user.id}','{interaction.user.name}',NOW(),'123','123456578')")
    

    await objectCodeChannel.channel.send(content=f"{interaction.user.mention}",embed=msg,file=file)

async def __createEmbedForContent(ContentType,Content,Redeem_Code,ContentRarity):
    embed : nextcord.embeds.Embed = None
    Rarity_message = ""
    match ContentRarity:
        case "uncommon":
            Rarity_message = "```ansi\n[\u001b[1;32mUncommon\u001b[0;0m]"
            pass
        case "rare":
            Rarity_message = "```ansi\n[\u001b[1;34mRare\u001b[0;0m]"
            pass
        case "epic":
            Rarity_message = "```ansi\n[\u001b[1;35mEpic\u001b[0;0m]"
            pass
        case "legendary":
            Rarity_message = "```ansi\n[\u001b[1;33mLegendary\u001b[0;0m]"
            pass
        case "RNGESUS":
            Rarity_message = "```ansi\n[\u001b[1;31mRNGESUS\u001b[0;0m][\u001b[1;36mRNGESUS\u001b[0;0m][\u001b[1;30mRNGESUS\u001b[0;0m]"
            pass
        case default:
            Rarity_message = "```ansi\n[\u001b[1;37mCommon\u001b[0;0m]"
            pass
    
    if ContentType == 0: #Money
        #print("T0")
        Anzahl = Content.get("Anzahl")
        if Content.get("MoneyType") == "Money":
            MoneyType = "Lass es \u001b[1;32mGeld\u001b[0;0m regnen!\n+\u001b[1;33m"+str(Anzahl)+"\u001b[0;0m$```"
        else:
            MoneyType = "Lass es \u001b[1;31mSchwarzgeld\u001b[0;0m regnen!\n+\u001b[1;33m"+str(Anzahl)+"\u001b[0;0m$```"
        Rarity_message = Rarity_message + "\n" + MoneyType
        embed = nextcord.embeds.Embed(title="Dein Booster-Code!",description=""+Rarity_message)
        embed.add_field(name="",value="Dein Code: ||"+str(Redeem_Code)+"|| (Klick zum Anzeigen)",inline=False)
        file = nextcord.File('img/gta-5-money.png', filename='money.png') 
        embed.set_image(url='attachment://money.png')

    elif ContentType == 1: # Cars
        #print("T1")
        CarName = Content.get("VehicleName")
        Rarity_message = Rarity_message + "\n" + "Schnall dich an und gib Gas mit deinem neuem "+CarName+"```"
        embed = nextcord.embeds.Embed(title="Dein Booster-Code!",description=Rarity_message)
        embed.add_field(name=f"",value="Dein Code: ||"+str(Redeem_Code)+"|| (Klick zum Anzeigen)",inline=False)
        file = nextcord.File('img/'+CarName+'.png', filename=CarName+'.png')
        embed.set_image(url='attachment://'+CarName+'.png')
        
    elif ContentType == 2: # Items
        #print("T2")
        items = Content.get("Arr_Items")
        items_count = Content.get("Arr_Anzahl")
        Rarity_message = Rarity_message + "\n\u001b[1;31mSanta Claus\u001b[0;0m hat dir ein Packet da gelassen:\n"
        for i in range(len(items)):
            Rarity_message = Rarity_message + "\nItem: \u001b[1;37m"+items[i]+"\u001b[0;0m | Anzahl: \u001b[1;37m"+str(items_count[i])+"\u001b[0;0m"
        embed = nextcord.embeds.Embed(title="Dein Booster-Code!",description=Rarity_message+"```")
        embed.add_field(name="",value="Dein Code: ||"+str(Redeem_Code)+"|| (Klick zum Anzeigen)",inline=False)
        file = nextcord.File('img/7eleven.png', filename='7eleven.png') 
        embed.set_image(url='attachment://7eleven.png')
        #print(items,'|',items_count,"|",Rarity_message,'|',file,'|',embed)

    embed.set_footer(text=BOT_FOOTERTEXT,icon_url=BOT_ICONLINK)
    return embed,file

## ------------------------------------------------
##Channel Functions
## ------------------------------------------------

async def __initUserChannels():
    mainCategory = bot.get_guild(SERVER_ID).get_channel(MAIN_CAT_ID)
    if mainCategory is None:
        print("Main category not found.")
        return
    for channel in mainCategory.channels:
        if channel.id == LOG_CHANNEL_ID:
            continue
        elif channel.id == MESSAGE_CHANNEL_ID:
            continue
        elif channel.id == ERROR_CHANNEL_ID:
            continue
        elif channel.type == nextcord.ChannelType.text:
            list_CodeChannels.append(CodeChannels(channel,bot.get_guild(SERVER_ID).get_member(int(channel.name))))
    return

async def createUserChannel(guild: nextcord.Guild, User: nextcord.Member):
    """
    Creates a private channel for a specific user within the guild or returns an existing one if found.

    Parameters:
        guild (nextcord.Guild): The guild where the private channel will be created or located.
        User (nextcord.Member): The user for whom the private channel is being created.

    Returns:
        CodeChannels: An object representing the newly created private channel or the existing one if found.

    Description:
        This function either creates a new private channel within the guild specifically for the given user or returns an existing one if found.
        - It first checks if there's already a private channel owned by the specified user.
            - If such a channel exists, it returns that channel object.
        - If no existing channel is found, it locates the main category where user channels are stored.
        - Then, it creates a new channel and sets permissions so that only the specified user can read and send messages in it.
        - After creating the channel and setting permissions, it creates an object to represent this channel and user pairing.
        - Finally, it adds this object to a list of user channels for tracking and returns the newly created channel object.
    """
    for channel in list_CodeChannels:
        if channel.owner == User:
            return channel
    mainCategory = guild.get_channel(MAIN_CAT_ID)
    channel = await __create_Channel(guild, User.id, mainCategory)
    await channel.set_permissions(User, read_messages=True, send_messages=True)
    ChannelObj = CodeChannels(channel,User)
    list_CodeChannels.append(ChannelObj)
    return ChannelObj

def __create_Overwrite(guild: nextcord.Guild) -> dict:
    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        guild.me: nextcord.PermissionOverwrite(read_messages=True,send_messages=True,embed_links=True)
    }
    for role in get_role(guild=guild,ids=BOT_CONTROL_ROLES):
        overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
    return overwrites

async def __create_Channel(guild: nextcord.Guild, name:str, CatergoryChannel: nextcord.CategoryChannel) -> nextcord.TextChannel:
    return await guild.create_text_channel(name, category=CatergoryChannel, overwrites=__create_Overwrite(guild))

## ------------------------------------------------
##Log Function
## ------------------------------------------------

async def log_msg(guild: nextcord.Guild, message: str, channel: nextcord.TextChannel = None):
    if channel is None:
        channel = guild.get_channel(LOG_CHANNEL_ID)
    logText = f"{BOT_NAME} | LOG: {message}. | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    await channel.send(logText)

## ------------------------------------------------
##Main Function
## ------------------------------------------------
if __name__ == "__main__":
    main()