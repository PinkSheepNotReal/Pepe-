import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class mod():
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, user):
        x = await self.bot.db.welcome.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        image = int(x['image'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(x['message'].replace('$name$', user.name).replace('$mention$', user.mention).replace('$server$', user.guild.name))
        if image == "on":
            img = Image.open("maxresdefault.jpg")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("American Captain.otf", 75)
            fontbig = ImageFont.truetype("American Captain.ttf", 100)
            draw.text((100, 0), "Welcome", (255, 255, 255), font=fontbig)
            draw.text((150, 125), "{}".format(user.name), (255, 255, 255), font=font)
            img.save(f'{user.id}.jpg')
            await send_channel.send(file=discord.File(f'{user.id}.jpg'))


    async def on_member_remove(self, user):
        em = discord.Embed(description=f"Goodbye **{user.name}**", color=0x1aff00, timestamp = datetime.datetime.utcnow())
        em.set_author(name=user, icon_url=user.avatar_url)
        x = await self.bot.db.leave.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(x['message'].replace('$name$', user.name).replace('$mention$', user.mention).replace('$server$', user.guild.name))   
   
    async def on_message_delete(self, message):
        em = discord.Embed(color=0x1aff00, timestamp = datetime.datetime.utcnow())
        em.add_field(name="Message deleted", value=message.content)
        em.set_author(name=message.author, icon_url=message.author.avatar_url)
        x = await self.bot.db.modlog.find_one({"id": str(message.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(embed=em)           

    async def on_message_edit(self, before, after):
        em = discord.Embed(color=0x1aff00, timestamp = datetime.datetime.utcnow())
        em.add_field(name="Before", value=before.content)
        em.add_field(name="After", value=after.content)
        em.set_author(name=before.author, icon_url=before.author.avatar_url)
        x = await self.bot.db.modlog.find_one({"id": str(before.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(embed=em)     

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**Choose `on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the welcome messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the welcome channel!**")
            await ctx.send("Please enter the message.\n\nVariables: \n$name$: The user's name.\n$mention$: Mention the user.\n$server$: The name of the server.")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                 return await ctx.send("Request timed out. Please try again.")
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel, "message": x.content}}, upsert=True)
            await ctx.send("Successfully turned on message")   
            await ctx.send("Do you want images? yes or no")
            try:
                y = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                 return await ctx.send("Request timed out. Please try again.")
            if y == "yes":
                await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"image": "on"}})
        if sort == "off":
            await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False, "message": None}}, upsert=True)
            await ctx.send("**I have turned off welcome messages**")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**Choose `on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the leave messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the welcome channel!**")
            await ctx.send("Please enter the message.\n\nVariables: \n$name$: The user's name.\n$mention$: Mention the user.\n$server$: The name of the server.")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                 return await ctx.send("Request timed out. Please try again.")
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel, "message": x.content}}, upsert=True)
            await ctx.send("Successfully turned on leave messages for this guild.")            
        if sort == "off":
            await self.bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False, "message": None}}, upsert=True)
            await ctx.send("**I have turned off leave messages**")           

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def modlog(self, ctx, sort=None):
        if sort == None:
            await ctx.send("**`on` or `off`**")
        if sort == "on":
            await ctx.send("**Please mention the channel to set the log messages in.**")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("**The time is up**")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("**Please mention the channel**")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("**Please mention the channel right**")
            await self.bot.db.modlog.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
            await ctx.send("**I have set the mod-log channel!**")
        if sort == "off":
            await self.bot.db.modlog.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": False} }, upsert=True )
            await ctx.send("**I have turned off modlog messages**")       
            
def setup(bot):
    bot.add_cog(mod(bot))
