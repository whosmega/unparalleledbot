from commons import sendMessage

leaderboardLimit = 100
firstEmoji = "🥇"
secondEmoji = "🥈"
thirdEmoji = "🥉"


def giveCash(client, member, amount):
    client.database.update_entry(table="BALANCE", key=member.id, keyfield="USERID", update=getCash(client, member) + amount, updatefield="CASH")

def takeCash(client, member, amount):
    giveCash(client, member, -amount)

def getCash(client, member):
    return client.database.get_entry(table="BALANCE", key=member.id, keyfield="USERID", value=0, valuefield="CASH")

async def displayCash(client, member, channel):
    cash = getCash(client, member)
    await sendMessage(client, channel, "Cash Balance", f"<@!{member.id}> you have **${cash}**!")

def clearCash(client, member):
    client.database.update_entry(key=member.id, keyfield="USERID", value=0, valuefield="CASH")

def getLeaderboard(client):
    return client.database.get_leaderboard(getfields="USERID, CASH", table="BALANCE", sortfields="CASH", limit=leaderboardLimit)

async def displayLeaderboard(client, channel):
    thing = getLeaderboard(client)
    lb = ""
    rank = 1
    for entry in thing:
        userid = entry[0]
        cash = entry[1]
        medal = None
        if rank == 1:
            medal = firstEmoji
        elif rank == 2:
            medal = secondEmoji
        elif rank == 3:
            medal = thirdEmoji

        column = f"\n**#{rank}**  {medal and medal + '  ' or ''}<@!{userid}> : **${cash}**"
        lb += column
        rank += 1

    await sendMessage(client, channel, "Leaderboard", lb)




