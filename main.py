from commons import *
from connect_four import *
from db_interface import db_interface
from currency import *
import asyncpraw as praw
import sys

prefix = "~"
helpMessage = f"""
**{prefix}help** : Displays all commands
**{prefix}balance** : Shows your cash balance
**{prefix}leaderboard** : Shows the top 100 wealthiest players 
**{prefix}meme** : Displays a random meme from r/memes!
"""

class Bot(discord.Client):
    
    database = None
    async def perform_update(self):
        pass

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(f"{prefix}help"))
        await self.setup_praw()
        print("Ready for input")

    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.content.startswith(prefix):
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
        elif args[0] == "help":
            await sendMessage(self, message.channel, "Commands", helpMessage)
        elif args[0] == "meme":
            meme = await self.r_memes.random()
            await sendComplexMessage(self, channel=message.channel, description=f"**{meme.title}**", image=meme.url)
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

    async def setup_praw(self):
        self.reddit = praw.Reddit(client_id=reddit_appid, client_secret = reddit_appsecret, password = reddit_password, user_agent = reddit_appname, username = reddit_username)
        self.r_memes = await self.reddit.subreddit("memes")

    def __init__(self, intents):
        self.database = db_interface("main.db")
        super().__init__(intents=intents)
        print("Initialized Class")

    def __del__(self):
        self.database.close()

    async def shut_down():
        await self.reddit.close()
        await self.logout()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True


bot = Bot(intents)
bot.run(token)

