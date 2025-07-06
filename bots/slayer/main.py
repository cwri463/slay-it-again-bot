import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
TREE = bot.tree

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0") or 0)
GUILD = discord.Object(id=GUILD_ID) if GUILD_ID else None

@TREE.command(name="ping", description="Check if the bot is alive", guild=GUILD)
async def ping_slash(inter: discord.Interaction):
    await inter.response.send_message("🏓 Pong!")

@bot.event
async def on_ready():
    if GUILD:
        TREE.clear_commands(guild=None)
        await TREE.sync(guild=None)
        synced = await TREE.sync(guild=GUILD)
        print("[SLASH] synced:", [c.name for c in synced])
    else:
        synced = await TREE.sync()
        print("[SLASH] synced (global):", [c.name for c in synced])
    print(f"[READY] {bot.user} online ✔")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set")
    bot.run(token)

