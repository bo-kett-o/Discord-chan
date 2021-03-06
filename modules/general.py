import discord
from discord.ext import commands
import typing
import io
from datetime import datetime
from extras import checks
import json

class general:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, message: commands.clean_content()):
        """Have the bot say something"""
        if not channel:
            return await ctx.send(message)
        auth = ctx.author
        checks = [
            auth.id not in self.bot.owners,
            not auth.guild_permissions.administrator,
            not auth.guild_permissions.manage_channels
        ]
        if any(checks):
            return await ctx.message.add_reaction("\u274c")
        else:
            await channel.send(message)

    @commands.command()
    async def ping(self, ctx):
        """Check bot ping and latency"""
        process_time = round(((datetime.utcnow()-ctx.message.created_at).total_seconds())*1000)
        e = discord.Embed(
            color=discord.Color.blurple()
        )
        e.add_field(
            name="**Latency:**",
            value=f"{round(self.bot.latency*1000)}ms"
        )
        e.add_field(
            name="**Process time:**",
            value=f"{process_time}ms",
            inline=False
        )
        e.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server"""
        invite0 = f"https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot"
        invite8 = f"https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot"
        message = f"**With perms:**\n<{invite8}>\n**Without perms (some things may not work):**\n<{invite0}>"
        await ctx.send(message)

    @commands.command(aliases=['msg'])
    @checks.serverowner_or_permissions(administrator=True)
    async def quote(self, ctx, user: discord.Member, *, message: str):
        """Send a message as someone else"""
        hook = await ctx.channel.create_webhook(name=user.display_name)
        await hook.send(message, avatar_url=user.avatar_url_as(format='png'))
        await hook.delete()

    @commands.command(aliases=['tobin'])
    async def tobinary(self, ctx, *, entry: str):
        """Convert text to binary"""
        final = ""
        for c in entry:
            x = ord(c)
            x = bin(x)
            x = x.replace('b', '')
            final += x + " "
        if len(final) > 1000:
            fp = io.BytesIO(final.encode('utf-8'))
            await ctx.send("Output too long, dmed your file")
            await ctx.author.send(file=discord.File(fp, 'results.txt'))
        else:
            await ctx.send(final)

    @commands.command(aliases=['fbin'])
    async def frombinary(self, ctx, *entry: str):
        """Convery binary to text"""
        final = ""
        for c in entry:
            x = int(c, 2)
            x = chr(x)
            final += x
        if len(final) > 1000:
            fp = io.BytesIO(final.encode('utf-8'))
            await ctx.send("Output too long, dmed your file")
            await ctx.author.send(file=discord.File(fp, 'results.txt'))
        else:
            final = final.replace('@', '@\u200b')
            await ctx.send(final)

    @commands.command()
    async def msgraw(self, ctx, id: int):
        """Get the raw message data"""
        try:
            message = await self.bot.http.get_message(ctx.channel.id, id)
        except:
            return await ctx.send("Invalid message id")
        if len(message['content']) >= 100:
            message['content'] = message['content'][:97] + "..."
        message['embeds'] = len(message['embeds'])
        json_msg = json.dumps(message, indent=4)
        json_msg = json_msg.replace("`", "`\u200b")
        await ctx.send(f"```json\n{json_msg}```")

def setup(bot):
    bot.add_cog(general(bot))