import discord
from discord.ext import commands
import os

# 【重要】トークンは直接書かず、環境変数からのみ読み込みます
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

IMAGE_DIR = "images"

GIF_MAP = {
    ":_1:": "_1.gif", ":_2:": "_2.gif", ":_3:": "_3.gif", ":_4:": "_4.gif",
    ":_5:": "_5.gif", ":_6:": "_6.gif", ":_7:": "_7.gif", ":_8:": "_8.gif",
    ":_9:": "_9.gif", ":10:": "10.gif", ":11:": "11.gif", ":12:": "12.gif",
    ":13:": "13.gif", ":14:": "14.gif", ":15:": "15.gif", ":16:": "16.gif",
    ":17:": "17.gif", ":18:": "18.gif", ":19:": "19.gif", ":20:": "20.gif",
    ":21:": "21.gif", ":22:": "22.gif", ":23:": "23.gif", ":24:": "24.gif",
    ":25:": "25.gif", ":26:": "26.gif", ":27:": "27.gif", ":28:": "28.gif",
    ":29:": "29.gif", ":30:": "30.gif", ":31:": "31.gif", ":32:": "32.gif",
    ":33:": "33.gif", ":34:": "34.gif", ":35:": "35.gif", ":36:": "36.gif",
    ":37:": "37.gif", ":38:": "38.gif", ":39:": "39.gif", ":40:": "40.gif", 
    ":41:": "41.gif", ":42:": "42.gif", ":43:": "43.gif", ":44:": "44.gif",
    ":45:": "45.gif", ":46:": "46.gif", ":47:": "47.gif", ":48:": "48.gif", 
    ":49:": "49.gif", ":50:": "50.gif", ":51:": "51.gif", ":52:": "52.gif",
    ":53:": "53.png", ":54:": "54.png", ":55:": "55.png", ":56:": "56.png",
    ":57:": "57.png", ":58:": "58.gif", ":59:": "59.gif", ":60:": "60.gif",
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    found_gifs = []
    for emoji, filename in GIF_MAP.items():
        if emoji in message.content:
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                found_gifs.append(path)

    if found_gifs:
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        reference = message.reference if message.reference else None
        for path in found_gifs:
            await message.channel.send(
                content=f"{message.author.mention}",
                file=discord.File(path),
                reference=reference,
                mention_author=True
            )

    await bot.process_commands(message)

def create_command(file_path):
    async def _cmd(ctx):
        if os.path.exists(file_path):
            await ctx.send(file=discord.File(file_path))
        else:
            await ctx.send("GIFが見つかりませんでした。")
    return _cmd

for emoji, filename in GIF_MAP.items():
    cmd_name = emoji.replace(":", "")
    full_path = os.path.join(IMAGE_DIR, filename)
    bot.add_command(commands.Command(create_command(full_path), name=cmd_name))

@bot.tree.command(name="all", description="対応しているスタンプ一覧を表示します")
async def all_cmd(interaction: discord.Interaction):
    text = " ".join(GIF_MAP.keys())
    await interaction.response.send_message(
        f"📚 **対応スタンプ一覧**\n{text}",
        ephemeral=True
    )

if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN が設定されていません。")
    else:
        bot.run(TOKEN)