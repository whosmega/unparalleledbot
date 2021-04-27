import discord
from credentials import *
from connect_four import *
from db_interface import db_interface

user_cache = {}     # Used to store users after 1 use for instant lookup
role_cache = {}     # Used to store roles after 1 use for instant lookup

def getUser(client, user_id):
    if not (user_id in user_cache.keys()):
        user_cache[user_id] = client.get_user(user_id)  # If the user isnt in cache, then add them
                                                        # for fast lookups

    return user_cache[user_id]

async def sendMessage(client, channel, title, message):
    await channel.send(embed=discord.Embed(
        title = title or "",
        description = message,
        colour = discord.Colour.blue()
    ))

def getMember(client, guild_id, user_id):

    
    if not (f"{user_id}-{guild_id}" in user_cache.keys()):
        guild = client.get_guild(guild_id)

        if not guild:
            return

        member = guild.get_member(user_id)
        if not member:
            return
        
        user_cache[f"{user_id}-{guild_id}"] = member


    return user_cache[f"{user_id}-{guild_id}"]

def addRoleCache(role_id):
    if not (role_id in role_cache.keys()):
        role_cache[role_id] = discord.Object(role_id)
        print(f"Added role {role_id} to role cache")
        return

    print("Skipped role add due to presence")

async def giveRole(member, role_id):
    addRoleCache(role_id)
    await member.add_roles(role_cache[role_id])
    print(f"Added role {role_id} to {member}")
    return True

async def removeRole(member, role_id):
    if not (role_id in role_cache.keys()):
        addRoleCache(role_id)
    await member.remove_roles(role_cache[role_id])
    print(f"Removed role {role_id} from {member}")
    return True

def getReactionRoleID(message_id, reaction_name):
    if not (message_id in reaction_roll_data.keys()):
        return None

    if not (reaction_name in reaction_roll_data[message_id].keys()):
        return None

    role_id = reaction_roll_data[message_id][reaction_name]
    return role_id

class Bot(discord.Client):
    prefix = "~"
    database = None
    async def perform_update(self):
        pass

    async def on_ready(self):
        await self.change_presence(activity=discord.Game("I've been told I'm a bot"))

        print("Ready for input")

    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.content.startswith(self.prefix):
            return

        args = message.content[1:].split()
        
        if args[0] == "balance":
            balance = self.database.get_cash_entry(message.author.id)
            await sendMessage(self, message.channel, "Cash Balance", str(balance))
            self.database.update_cash_entry(message.author.id, balance + 100)
    async def on_raw_reaction_add(self, payload):
        role_id = getReactionRoleID(payload.message_id, payload.emoji.name)

        if not role_id:
            return
        
        await giveRole(getMember(self, payload.guild_id, payload.user_id), role_id)
        

    async def on_raw_reaction_remove(self, payload):
        role_id = getReactionRoleID(payload.message_id, payload.emoji.name)

        if not role_id:
            return
        await removeRole(getMember(self, payload.guild_id, payload.user_id), role_id)

    async def on_member_join(self, member):
        await giveRole(member, member_id)

    def __init__(self, intents):
        self.database = db_interface("main.db")
        super().__init__(intents=intents)
        print("Initialized Class")

    def __del__(self):
        self.database.close()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = Bot(intents)
bot.run(token)



