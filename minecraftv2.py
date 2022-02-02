# a second iteration on the minecraft server checker tht will have an automatic server checker and statistics n shit

from discord.embeds import Embed
from discord.ext import commands , tasks
from Tiddleton import RoleChecks, RoleIDs
from mcstatus import MinecraftServer as MCS

import discord
import os , json , re , datetime
import socket

"""
json structure : 

{
    "servers" : [{
        "IpAdress" : <ip>,
        "messageID" : <message id>,
        "channelID" : <channel id>
        } , ...],
    "playerData" : 
        [{
            "username" : <username>,
            "totalMinutes" : <minutes>
            
        } , ...]
    }
}
"""

#this doesnt really need to be here but its cool so fuck you :)
def XORencrypt(inp : str) -> str:
    #not the most secure thing in the world but its better than nothing
    #NOTE goes both ways, Encrypted <-> Decrypted
    passCode = os.environ.get("XORPASSCODE")
    assert passCode != None , "passcode doesnt exsist"
    cryptStr = ""
    for i , c in enumerate(inp):
        if i >= len(passCode):
            i -= len(passCode)
        cryptStr += chr(ord(c) ^ ord(passCode[i]))
    return cryptStr          
    
def isIPaddr(ipAdress) -> bool:
	return True
    #matc = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.:[0-9]+" , ipAdress)
    #return matc != None
    
KNOWNPLAYERS = []  # populate this with player objects on load
SERVERS = []       # populate this with server objects on load

LOOPMINUTES = 1
    
class DataClass:
    # uses the dir() method and filters dunders to save any object to a json file
    #NOTE the names of the attributes are what will be used as keys in the dictionary
    
    def JSONify(self) -> dict:
        allAttribs = dir(self)
        dataDict = {}
        for attr in allAttribs:
            attr : str
            if not attr.startswith("__"):
                temp = getattr(self , attr)
                if type(temp) == type(self.JSONify):
                	continue
                dataDict[attr] = temp
        return dataDict
    
    def populateFromDict(self , attribs : dict):
        for attr in attribs.keys():
            setattr(self, attr , attribs[attr])

class Player(DataClass):
    def __init__(self , username : str = None) -> None:
        super().__init__()
        self.username = username
        self.totalMinutes = 0
        
    def isMe(self , name) -> bool:
        return name == self.username

    def __str__(self) -> str:
    	return f"Player : {self.username}"

class Server(DataClass):
    def __init__(self , ipAdress : str = None , messageid : int = None , channelID : int = None) -> None:
        super().__init__()
        self.IpAdress = ipAdress
        self.messageID = messageid
        self.channelID = channelID
        
    def query(self) -> dict:
        #gets all of the information about a server
        # {"error" : <err status, none for no error> , "online" : <bool> , "players" : [<player object> , ...] , "maxPlayers" : <maxPlayers> , "versionName" : <versionName>}
        data = {"error" : None , "online" : True , "players" : [] , "maxPlayers" : 0 , "versionName" : "unkown"}
        
        try:
            server = MCS.lookup(self.IpAdress)
        except socket.gaierror():
            data["error"] = "Invalid server adress"
            return data
        
        try:
            status = server.status()
        except BaseException as e:
            #get proper error information includeing if the server is offline
            if type(e) == type(socket.gaierror()):
                data["error"] = "Invalid server adress"
                return data
            
            if e.error.errno == 111:
                data["error"] = "connection refused"
                return data
            elif e == socket.timeout():
                data["online"] = False
            else:
                data["error"] = "unexpected error"
                return data 
        
        if data["online"]:
            rawData = status.raw
            playerData = rawData["players"]
            versionData = rawData["version"]
            
            try:
                playerNames = playerData["sample"]
            except KeyError:
                playerNames = []
                
            players = []
            for name in playerNames:
                name = name["name"]
                player = None
                for p in KNOWNPLAYERS:
                    p : Player
                    if p.isMe(name):
                        player = p
                if player == None:
                    newPlayer = Player(name)
                    KNOWNPLAYERS.append(newPlayer)
                    player = newPlayer
                players.append(player)
            data["players"] = players
            data["maxPlayers"] = playerData["max"]
            data["versionName"] = versionData["name"]
        return data
    
    def getEmbed(self , data) -> Embed:
        onlineCol = 0x00ff00
        offlineCol = 0xff0000
        title = f"Server satus for : {self.IpAdress}"
        if data["error"] != None:
            desc = f"There was an error : \n```{data['error']}```"
        else:
            if data["online"]:
                desc = f"Players : {len(data['players'])}/{data['maxPlayers']}\nVersion : {data['versionName']}\n\n```"
                for p in range(len(data["players"])):
                    desc += data["players"][p].username + "\n"
                desc += "```"
            else:
                desc = "The server is offline"
        desc += f"\nlast updated : {datetime.datetime.now()}"
        return Embed(title = title , description = desc , color = onlineCol if data["online"] else offlineCol)
                
        
class JSONhandler:
    def __init__(self) -> None:
        self.filePath = "minecraft/mcDat.json"
        self.__checkDB()
        
    def __checkDB(self):
        #checks the database has the required sections
        assert os.path.exists(self.filePath) , "file path doesnt exsist"
        
        with open(self.filePath , "r") as F:
            data = json.load(F)
        if "servers" not in data.keys():
            data["servers"] = []
        
        if "playerData" not in data.keys():
            data["playerData"] = []
        with open(self.filePath , "w") as F:
            json.dump(data , F)
    
    def update(self):
        #takes the global lists and dumps them to the DB
        data = {}
        data["servers"] = [s.JSONify() for s in SERVERS]
        data["playerData"] = [p.JSONify() for p in KNOWNPLAYERS]

        with open(self.filePath , "w") as F:
            json.dump(data , F)
    
    def load(self):
        #opens the DB and loads it into the gloabl lists
        with open(self.filePath , "r") as F:
            data = json.load(F)
        
        #load servers
        rawServers = data["servers"]
        for s in rawServers:
            blank = Server()
            blank.populateFromDict(s)
            SERVERS.append(blank)
            
            
        #load known players
        rawPlayers = data["playerData"]
        for p in rawPlayers:
            blank = Player()
            blank.populateFromDict(p)
            KNOWNPLAYERS.append(blank)



class MinecraftV2(commands.Cog):
    def __init__(self , bot) -> None:
        self.bot : commands.Bot = bot
        self.jsonHandle = JSONhandler()
        self.jsonHandle.load()
        self.serverCheckLoop.start()
        
    #@RoleChecks.is_Admin()
    @commands.command()
    async def addServer(self , ctx , ipAdress : str , channel : discord.TextChannel):
        "create and add a new server"
        assert isIPaddr(ipAdress) , f"invalid ipAdress {ipAdress}"
        assert not any([s.ipAdress == ipAdress for s in SERVERS]) , "server already exsists"
        serv = Server(ipAdress = ipAdress , channelID = channel.id)
        data = serv.query()
        mess = await channel.send(embed = serv.getEmbed(data))
        serv.messageID = mess.id
        SERVERS.append(serv)
    
    #@RoleChecks.is_Admin()
    @commands.command()
    async def removeServer(self , ctx , ipAdress : str):
        "Removes a server from the database and deletes the message"
        assert isIPaddr(ipAdress) , f"invalid ipAdress {ipAdress}"
        for s in SERVERS:
            if s.IpAdress == ipAdress:
                #get message and delete
                SERVERS.pop(SERVERS.index(s))
                channel : discord.TextChannel = self.bot.fetch_channel(s.channelID)
                mess : discord.Message = await channel.fetch_message(s.messageID)
                await mess.delete()
                return
        await ctx.send("That server doesnt exsist")
        
        
    @tasks.loop(minutes = LOOPMINUTES)
    async def serverCheckLoop(self):
        #main loop that queries each server and modifies its message with the new data
        for s in SERVERS:
            channel : discord.TextChannel = await self.bot.fetch_channel(s.channelID)
            assert channel != None , f"problem with the channel id : {s.channelID}"
            data = s.query()
            mess : discord.Message = await channel.fetch_message(s.messageID)
            assert mess != None , f"problem with message id : {s.messageID}"
            if mess == None:
                print(f"[ERROR] minecraft server [{s.IpAdress}]'s message is not working")
                continue
            await mess.edit(embed = s.getEmbed(data))
            
            for p in data["players"]:
                p.totalMinutes += LOOPMINUTES
        self.jsonHandle.update()
    
    
    def cog_unload(self):
        "special unloading procedure"
        print("unloading Minecraft")
        self.serverCheckLoop.stop()
        self.jsonHandle.update()
        
def setup(bot):
    bot.add_cog(MinecraftV2(bot))