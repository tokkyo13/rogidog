import os
import time
import discord
from gtts import gTTS


# 読み上げ用 channel id を設定
# text-to-speech の id
# channel の id は discord で開発者モードをONにすると見れるようになる
READ_CHANNEL_ID = 845172576673071114


# 音声の再生先 channel id を設定
# room 101 の id
# channel の id は discord で開発者モードをONにすると見れるようになる
SPEAK_CHANNEL_ID = 697839608565858357


client = discord.Client()


# gTTS
# https://github.com/pndurette/gTTS
# google translate の内部 API にタダ乗りする音声合成ライブラリ
def google_tts(text: str) -> None:
    tts = gTTS(text, lang="ja")
    tts.save("/tmp/message.mp3")

# メッセージが送信されたら実行
@client.event
async def on_message(message):
    # チャンネルが読み上げ用でなければ無視
    if message.channel.id != READ_CHANNEL_ID:
        return

    # 発言者が bot なら無視
    if message.author.bot:
        return

    # 発言者がボイスチャンネルでミュート状態でなければエラーメッセージ
    if message.author.voice is None:
        return

    # voice channel に接続していなければ接続する
    if message.guild.voice_client is None:
        await message.guild.get_channel(SPEAK_CHANNEL_ID).connect()

    # いま音声を再生中だったら待つ
    while message.guild.voice_client.is_playing():
        time.sleep(1)
        continue

    # gTTS でメッセージのテキストから音声ファイルを作り
    google_tts(message_casted)
    # ffmpeg で AudioSource に変換
    audio_source = discord.FFmpegPCMAudio("/tmp/message.mp3")

    # 作ったオーディオソースを再生
    message.guild.voice_client.play(audio_source)


token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)