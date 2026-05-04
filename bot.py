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
    ":13:": "13.gif", ":14:": "14.gif", ":15:": "15.gif", ":16:": "16.png",
    ":17:": "17.png", ":18:": "18.gif", ":19:": "19.png", ":20:": "20.gif",
    ":21:": "21.png", ":22:": "22.gif", ":23:": "23.gif", ":24:": "24.png",
    ":25:": "25.png", ":26:": "26.png", ":27:": "27.png", ":28:": "28.png",
    ":29:": "29.png", ":30:": "30.gif", ":31:": "31.png", ":32:": "32.png",
    ":33:": "33.gif", ":34:": "34.png", ":35:": "35.gif", ":36:": "36.png",
    ":37:": "37.gif", ":38:": "38.png", ":39:": "39.png", ":40:": "40.png", 
    ":41:": "41.png", ":42:": "42.png", ":43:": "43.png", ":44:": "44.gif",
    ":45:": "45.png", ":46:": "46.gif", ":47:": "47.png", ":48:": "48.gif", 
    ":49:": "49.gif", ":50:": "50.png", ":51:": "51.png", ":52:": "52.png",
    ":53:": "53.png", ":54:": "54.png", ":55:": "55.png", ":56:": "56.png",
    ":57:": "57.png", ":58:": "58.png", ":59:": "59.png", ":60:": "60.png",
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