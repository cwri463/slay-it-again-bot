"""
Slay-It-Again bot • MVP skeleton
--------------------------------
  /ping   – sanity check (guild-scoped if DISCORD_GUILD_ID is set)
"""

import os
import discord
from discord.ext import commands
from discord import app_commands


import asyncio, asyncpg, os, discord

DB_URL = os.getenv("DATABASE_URL")

async def scoreboard_embed():
    pool = await asyncpg.create_pool(DB_URL)
    query = """SELECT player, sum(points) AS pts
               FROM loot_events GROUP BY player ORDER BY pts DESC LIMIT 10"""
    rows = await pool.fetch(query)
    embed = discord.Embed(
        title="Slay-That-Again – Top 10",
        colour=0x77ff77
    )
    for idx, r in enumerate(rows, 1):
        embed.add_field(name=f"#{idx}  {r['player']}", value=f"{r['pts']} pts", inline=False)
    return embed

@tree.command(name="scoreboard", description="Show current leaderboard")
async def scoreboard_cmd(inter: discord.Interaction):
    await inter.response.defer()
    embed = await scoreboard_embed()
    await inter.followup.send(embed=embed)


# ── Intents & Bot object ────────────────────────────────────────────
intents = discord.Intents.default()
bot     = commands.Bot(command_prefix="!", intents=intents)
TREE    = bot.tree                     # handy alias

# ── Per-guild fast sync (optional) ──────────────────────────────────
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0") or 0)
GUILD    = discord.Object(id=GUILD_ID) if GUILD_ID else None

# ── /ping command ───────────────────────────────────────────────────
@TREE.command(name="ping",
              description="Check if the bot is alive",
              guild=GUILD)             # None → global
async def ping_slash(inter: discord.Interaction):
    await inter.response.send_message("🏓 Pong from **Slay-It-Again**!")

# ── on_ready: wipe globals → sync guild cmds (prevents duplicates) ──
@bot.event
async def on_ready():
    if GUILD:
        TREE.clear_commands(guild=None)
        await TREE.sync(guild=None)        # push empty global set
        synced = await TREE.sync(guild=GUILD)
    else:
        synced = await TREE.sync()         # global (may take 1 h to show)
    print("[SLASH] synced:", [c.name for c in synced])
    print(f"[READY] {bot.user} online ✔")

# ── Main entry ──────────────────────────────────────────────────────
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set")
    bot.run(token)
