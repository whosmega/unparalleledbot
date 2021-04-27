import discord
from credentials import *

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