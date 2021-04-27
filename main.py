from commons import *
from connect_four import *
from db_interface import db_interface
from currency import *

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
        
        if len(args) <= 0:
            return

        if args[0] == "balance":
            if len(args) == 2 and len(args[1]) >= 4:
                id = args[1].strip("<").strip(">").strip("@").strip("!")

                if id.isnumeric():
                    member = getMember(self, message.guild.id, int(id))
                    if not member:
                        return
                    await displayCash(self, member, message.channel)
                    return

            await displayCash(self, message.author, message.channel)
            # giveCash(self, message.author, 100)
        elif args[0] == "leaderboard":
            await displayLeaderboard(self, message.channel)
        else:
            await sendMessage(self, message.channel, "Unknown Command!", "")
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



