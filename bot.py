import discord
from discord.ext import commands
import os
import sys

# --- Config ---
TOKEN = ''
CHANNEL_ID = 1295315064366301254
PLAYSTORE_URL = 'https://play.google.com/store/apps/details?id=com.voidware.voidcaller&hl=en&gl=US'
APP_NAME = 'Voidcaller'
APP_ICON = 'https://play-lh.googleusercontent.com/-d3qaclKnc4Vnrdpt8CP9799qzBtgBec-HhDXrltHxVLYc0psgpSge0f9rulaN9GS1o'
ROLE_NAME = '📝 │ App-Testers'
# ----------------

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def post_update(ctx, *, arg):
    try:
        if "|" not in arg:
            await ctx.send("❌ Format: `!post_update <version> | <changelog>`")
            return

        version, changelog = [x.strip() for x in arg.split("|", 1)]

        embed = discord.Embed(
            title=APP_NAME,
            description=f"🔧 {changelog}",
            color=discord.Color.green()
        )
        embed.add_field(name="Version", value=f"`{version}`", inline=False)
        embed.add_field(name="Go to Play Store", value=f"[Click here]({PLAYSTORE_URL})", inline=False)
        embed.set_thumbnail(url=APP_ICON)

        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            await ctx.send("❌ Channel not found.")
            return

        # Find the role to mention
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
        if not role:
            await ctx.send(f"❌ Role '@{ROLE_NAME}' not found.")
            return

        # Send the message with role mention
        await channel.send(content=role.mention, embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def shutdown(ctx):
    await ctx.send("🛑 Shutting down...")
    await bot.close()

@bot.command()
async def restart(ctx):
    await ctx.send("🔄 Restarting...")
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

bot.run(TOKEN)
