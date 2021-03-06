import discord, datetime
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
    
bot=commands.Bot(command_prefix='p!')
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.economy")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.giveaway")
bot.load_extension("cogs.music")

@bot.event
async def on_ready():
    print("Im online") 
    await bot.change_presence(activity=discord.Game(name="p!help"))
    
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My commands", color=0x9b9dff)
    embed.add_field(name="Info", value="`help`, `info`, `invite`", inline=False)
    embed.add_field(name="Fun", value="`roast`, `face`, `lenny`, `tableflip`, `dog`", inline=False)
    embed.add_field(name="Economy", value="`openaccount`, `earn`, `bal`, `daily`", inline=False)
    embed.add_field(name="Images", value="`rip`, `achievement`, `avatar`", inline=False)
    embed.add_field(name="Moderation", value="`welcome`, `leave`, `modlog`, `antiinvites`, `kick`, `ban`, `purge`", inline=False)
    embed.add_field(name="Music", value="`join`, `play`, `nowplaying`, `playlist`, `pause`, `stop`, `resume`, `empty`")
    embed.add_field(name="Giveaway", value="`start`", inline=False)
    embed.add_field(name="Utility", value="`8ball`, `serverinfo`, `userinfo`", inline=False)
    embed.set_footer(text="I´m a very new bot and in early development, there will come A LOT more commands!")
    await ctx.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    embed1=discord.Embed(title="New server!", description=guild.name, color=0x1aff00, timestamp = datetime.datetime.utcnow())
    embed1.set_thumbnail(url=guild.icon_url)
    await bot.get_channel(457180373466480640).send(embed=embed1)

@bot.event
async def on_guild_remove(guild):
    embed1=discord.Embed(title="Left server!", description=guild.name, color=0xff1c1c, timestamp = datetime.datetime.utcnow())
    embed1.set_thumbnail(url=guild.icon_url)
    await bot.get_channel(457180373466480640).send(embed=embed1)    

def has_role_in_my_server(name):
    def wrapper(ctx):
        server = bot.get_guild(455305359645736971)
        role = discord.utils.get(server.roles, name=name)
        user = discord.utils.get(server.members, id=ctx.author.id)
        if not user or not role: return False
        return role in user.roles
    return commands.check(wrapper)

@bot.command()
@has_role_in_my_server("premium")
@commands.cooldown(1, 60, commands.BucketType.user)
async def repeat(ctx, times: int,*, content : str):
    for i in range(times):
        await ctx.send(content)
        
db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot    
    
if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))
