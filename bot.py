import discord
from discord.ext import commands
from discord import app_commands
import os

# Renderの環境変数から取得、なければ直接入力（セキュリティ上環境変数推奨）
TOKEN = os.getenv("DISCORD_TOKEN") or "MTQ1NzgwNzUxMzE2Nzg1NTg3MQ.GiBW7Z.Y5iN9Yi9E6wQk3BuqXpeLh9xxNsTaevFu28lJI"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# 画像フォルダのパス（相対パス）
IMAGE_DIR = "images"

# GIF/画像マップの定義
GIF_MAP = {
    ":_1:": "_1.gif", ":_2:": "_2.gif", ":_3:": "_3.gif", ":_4:": "_4.gif",
    ":_5:": "_5.gif", ":_6:": "_6.gif", ":_7:": "_7.gif", ":_8:": "_8.gif",
    ":_9:": "_9.gif", ":10:": "10.gif", ":11:": "11.gif", ":12:": "12.gif",
    ":13:": "13.gif", ":14:": "14.gif", ":15:": "15.gif", ":16:": "16.gif",
    ":17:": "17.gif", ":18:": "18.gif", ":19:": "19.gif", ":20:": "20.gif",
    ":21:": "21.gif", ":22:": "22.gif", ":23:": "23.gif", ":24:": "24.gif",
    ":25:": "25.gif", ":26:": "26.gif", ":27:": "27.gif", ":28:": "28.gif",
    ":29:": "29.gif", ":30:": "30.gif", ":35:": "35.gif", ":41:": "41.gif",
    ":42:": "42.gif", ":43:": "43.gif", ":44:": "44.gif", ":45:": "45.gif",
    ":46:": "46.gif", ":47:": "47.gif", ":48:": "48.gif", ":49:": "49.gif",
    ":50:": "50.gif", ":51:": "51.gif", ":52:": "52.gif",
    ":53:": "53.png", ":54:": "54.png", ":55:": "55.png", ":56:": "56.png",
    ":57:": "57.png", ":58:": "58.gif", ":59:": "59.gif", ":60:": "60.gif",
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# メッセージ内の絵文字検出機能
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
        # メッセージ削除
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        reference = message.reference if message.reference else None
        
        # 検出されたすべてのGIFを送信
        for path in found_gifs:
            await message.channel.send(
                content=f"{message.author.mention}",
                file=discord.File(path),
                reference=reference,
                mention_author=True
            )

    await bot.process_commands(message)

# 個別コマンド（/_1 など）を動的に登録
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

# スラッシュコマンド /all
@bot.tree.command(name="all", description="対応しているスタンプ一覧を表示します")
async def all_cmd(interaction: discord.Interaction):
    text = " ".join(GIF_MAP.keys())
    await interaction.response.send_message(
        f"📚 **対応スタンプ一覧**\n{text}",
        ephemeral=True
    )

bot.run(TOKEN)