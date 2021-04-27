from commons import sendMessage

leaderboardLimit = 100
firstEmoji = "🥇"


def giveCash(client, member, amount):
    client.database.update_entry(table="BALANCE", key=member.id, keyfield="USERID", update=getCash(client, member) + amount, updatefield="CASH")

def takeCash(client, member, amount):
    giveCash(client, member, -amount)

def getCash(client, member):
    return client.database.get_entry(table="BALANCE", key=member.id, keyfield="USERID", value=0, valuefield="CASH")

async def displayCash(client, member, channel):
    cash = getCash(client, member)
    await sendMessage(client, channel, "Cash Balance", f"<@!{member.id}> you have ${cash}!")

def clearCash(client, member):
    client.database.update_entry(key=member.id, keyfield="USERID", value=0, valuefield="CASH")

def getLeaderboard(client):
    return client.database.get_leaderboard(getfields="USERID, CASH", table="BALANCE", sortfields="CASH", limit=leaderboardLimit)

async def displayLeaderboard(client, channel):
    thing = getLeaderboard(client)



