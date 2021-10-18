import os, datetime
from discord.utils import get
from discord.ext import commands

def WriteLog(user, content):
  with open("./BotData/Log.txt", "a") as f:
    now = datetime.datetime.now().strftime("[%d/%H/%y %T]")
    f.write(f"{now}>> {user} : {content}\n")

class BotDataError(Exception) :
  def __init__(self, *args):
    super().__init__(*args)

class RoleIDs():
  IDList = list(map(
    int,
    os.environ["RoleIDs"].split('/')
  ))

  IT = IDList[0]
  Admin = IDList[1]
  Police = IDList[2]

  IDTable = {
    "IT" : IT,
    "Admin" : Admin,
    "Police" : Police 
  }

class RoleChecks():
  def is_IT(context):
    return get(context.guild.roles, id=RoleIDs.IT) in context.author.roles
  
  def is_Police(context):
    return get(context.guild.roles, id=RoleIDs.Police) in context.author.roles

  def is_Admin(context):
    return get(context.guild.roles, id=RoleIDs.Admin) in context.author.roles
