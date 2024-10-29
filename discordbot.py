import discord
from discord.ext import commands
import interactions
import asyncio

import unicodedata
import os
import datetime
import time
import re
import requests
import wave

import AIvoice
import CeVIOAI
import all
import DeepLAPI
import preset
from pyokaka import okaka

#カレント移動
os.chdir(os.path.dirname(__file__))

# アクセストークン
TOKEN =  # アクセストークンを入力してください str

# サーバーID
server_id = # ここに使用したいサーバーのをIDを入力してください int

# BOTユーザーID
bot_id = # 使用するBOTのユーザーIDを入力してください int

def load_settings():
    # BOT設定データ
    global configs_data
    global character_limit
    global voice_entry_exit_read
    global voice_entry_str_front
    global voice_entry_str_back
    global voice_exit_str_front
    global voice_exit_str_back

    configs_data = preset.config_change()
    character_limit = configs_data["character_limit"] # 読み上げ上限文字数
    # ボイスチャットの入退出の読み上げ
    voice_entry_exit_read = configs_data["voice_entry_exit_read"] # 読み上げのON OFF
    voice_entry_str_front = configs_data["voice_entry_str_front"] # 入室時名前の前に追加する文字
    voice_entry_str_back = configs_data["voice_entry_str_back"] # 入室時名前の後に追加する文字
    voice_exit_str_front = configs_data["voice_exit_str_front"] # 退出時名前の前に追加する文字
    voice_exit_str_back = configs_data["voice_exit_str_back"] # 退出時名前の後に追加する文字

    if voice_entry_str_front is None:
        voice_entry_str_front = ""
    if voice_entry_str_back is None:
        voice_entry_str_back = ""
    if voice_exit_str_front is None:
        voice_exit_str_front = ""
    if voice_exit_str_back is None:
        voice_exit_str_back = ""

# 関数
# ひらがな カタカナ 漢字が含まれている場合Trueを返す
def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def dt_now():
    return(datetime.datetime.now())

def Emoji_information(sentence):
    re_sentence = ""
    split_sentence = sentence.split(">")
    for i in split_sentence:
        i = i.strip()
        if i.startswith("<") == True:
            if i.startswith("<a:") == True:
                extract_sentence = re.search(r'<a:(.+):',i).group(1)
            elif i.startswith("<:") == True:
                extract_sentence = re.search(r'<:(.+):',i).group(1)
            re_sentence += extract_sentence
        else:
            re_sentence += i
    return(re_sentence)


# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

inter = interactions.Client(token=TOKEN, disable_sync=False)

# 起動時に動作する処理
@bot.event
async def on_ready():
    print("ログインしました。")
    await bot.change_presence(status=discord.Status.online, activity=None)


# 切断時
@bot.event
async def on_disconnect():
    print("切断されました")

def voice_create(after_mes_text, preset_data_id):
    preset_data = preset.VoicePreset_json_get(preset_data_id)
    print(preset_data)
    generation_software = preset_data["generation_software"]
    if generation_software == "A.I.VOICE":
        AIvoice.create(after_mes_text, preset_data)
    elif generation_software == "CeVIO AI":
        generate_re = CeVIOAI.create(after_mes_text, preset_data)
        if generate_re == False:
            return
    else:
        raise ValueError("ボイスプリセットエラー")
    return

async def reproduction(message, after_mes_text, channel=None, voice=None):
    if message is False:
        preset_data_id = bot_id
        play_channel = channel.guild.voice_client.play
    else:
        preset_data_id = message.author.id
        play_channel = message.guild.voice_client.play

    if voice is True:
        preset_data_id = 0

    voice_create(after_mes_text, preset_data_id)

    # 音声ファイルを流す
    FILE_PATH = "output.wav"
    # 読み込みモードでWAVファイルを開く
    with wave.open(FILE_PATH,  'rb') as wr:
        # 長さ情報取得
        fr = wr.getframerate()
        fn = wr.getnframes()

    play_channel(discord.FFmpegPCMAudio("output.wav"))

    # 取得した長さ分待つ
    time.sleep(fn / fr)

# メッセージ受信時に動作する処理
@bot.listen()
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # おみくじ
    if message.content == "おみくじ":
        retu = all.omikuzi()
        await message.channel.send(retu[0])

    # さいころ
    dice = list(str(message.content))
    if "d" in dice or "D" in dice or "ｄ" in dice or "Ｄ" in dice:
                    # 入力文字化
                    wait_message = str(message.content)
                    if "https://" not in wait_message and "http://" not in wait_message:
                        if False == is_japanese(wait_message):
                            say = all.dice(wait_message)
                            if say != "入力形式が違います。":
                                await message.reply(say)

    # ボイスチャンネル
    # 接続用
    if message.content == f"<@{bot_id}>":
        if message.author.voice is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません。")
            return
        
        await message.author.voice.channel.connect()
        await message.channel.send("接続しました。")

    # 切断用
    elif message.content == f"<@{bot_id}> cut" or message.content == f"<@{bot_id}>cut":
        if message.guild.voice_client is None:
            return

        # 切断する
        await message.guild.voice_client.disconnect()
        await message.channel.send("切断しました。")

    #　音声生成用
    # 接続時のみ生成
    print(message.content)
    if message.guild.voice_client is None:
        pass
    else:
        # urlとメンションは除外
        if "https://" in message.content or "http://" in message.content or "<@" in message.content or message.content == "":
            return

        # 音声生成
        try:
            before_mes_text = message.content
            # 絵文字の名称のみ
            after_conversion = Emoji_information(before_mes_text)
            # ローマ字変換
            romaji_to_kana = okaka.convert(after_conversion)
            # 文字数制限
            after_mes_text = romaji_to_kana[0:character_limit]
            if len(romaji_to_kana) != len(after_mes_text):
                after_mes_text += "以下略"
            await reproduction(message, after_mes_text)

        except requests.exceptions.ConnectionError:
            print("ConnectionResetError")
            pass
        except discord.ClientException as e:
            pass
        except Exception:
            pass

# ボイスチャンネル入退出検知
@bot.event
async def on_voice_state_update(member, before, after):
    # 自動切断用
    try:
        if len([i.name for i in after.channel.members]) == 1:
            await member.voice.channel.connect()
    except Exception:
        pass
    try:
        members = [i.name for i in before.channel.members]
        if len(members) == 1:
            await member.guild.voice_client.disconnect()
            await bot.get_channel(before.channel.id).send("切断しました。")
    except:
            pass

    # 入退出通知
    try:
        if before.channel is None and after.channel is not None:
            # ボイスチャンネルに接続した場合
            channel = after.channel
            c = (f"{voice_entry_str_front}{member.display_name}{voice_entry_str_back}")

        elif before.channel is not None and after.channel is None:
            # ボイスチャンネルから退出した場合
            channel = before.channel
            c = (f"{voice_exit_str_front}{member.display_name}{voice_exit_str_back}")

        await channel.send(c)
        if channel.guild.voice_client is None:
            return
        global voice_entry_exit_read
        if voice_entry_exit_read is True:
            await reproduction(False, c, channel)

    except Exception:
        pass

# 音声生成文字数等設定
@inter.command(
    name="bot_settings_change",
    description="BOT設定変更",
    scope=server_id,
    options = [
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="setting_name",
        description="設定ボイス",
        required=True,
        choices=[
            interactions.Choice(name="読み上げ上限", value="character_limit"),
            interactions.Choice(name="入退出読み上げ", value="voice_entry_exit_read"),
            interactions.Choice(name="入室ユーザー名前", value="voice_entry_str_front"),
            interactions.Choice(name="入室ユーザー名後", value="voice_entry_str_back"),
            interactions.Choice(name="退出ユーザー名前", value="voice_exit_str_front"),
            interactions.Choice(name="退出ユーザー名後", value="voice_exit_str_back"),
            interactions.Choice(name="設定データ出力", value="output_sttings_data"),
            ], 
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="value1",
            description="文字数",
            required=False,
        ),
        interactions.Option(
            type=interactions.OptionType.BOOLEAN,
            name="value2",
            description="ブール値",
            required=False,
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="value3",
            description="文字",
            required=False,
        ),
    ],
)
async def bot_settings_change(ctx, setting_name, value1=None, value2=True, value3=None):
    try:
        if setting_name == "output_sttings_data":
            await ctx.send(F"{configs_data}", ephemeral=True)
            return
        elif setting_name == "character_limit":
            if value1 is None:
                await ctx.send(F"値が不正です", ephemeral=True)
            change_value = value1
        elif setting_name == "voice_entry_exit_read":
            change_value = value2
        elif setting_name in ["voice_entry_str_front", "voice_entry_str_back", "voice_exit_str_front", "voice_exit_str_back"]:
            change_value = value3
        
        preset.config_change(setting_name, change_value)
        load_settings()
        await ctx.send(F"{setting_name}を{change_value}に変更しました", ephemeral=True)
        
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\nbot_setting_change\n{e}")

# ボイス変更
@inter.command(
    name="voicepreset",
    description="ボイス変更",
    scope=[server_id,],
    options = [
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="setting",
        description="設定ボイス",
        required=True,
        choices=[
            interactions.Choice(name="さとうささら", value="さとうささら"),
            interactions.Choice(name="すずきつづみ", value="すずきつづみ"),
            interactions.Choice(name="栗田まろん", value="栗田まろん"),
            interactions.Choice(name="紅桜ショウガ", value="紅桜ショウガ"),
            ], 
        ),
    ],
)
async def voicepreset(ctx, setting: str):
    try:
        preset.VoicePreset_json_write(ctx.author.id, setting)
        await ctx.send(F"設定ボイスを{setting}に変更しました", ephemeral=True)
        return
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\nsetting:{setting}\n{e}")

# CeVIOAIボイス設定変更
@inter.command(
    name="cevioai_change_voice_settings",
    description="CeVIOボイス設定変更",
    scope=[server_id],
    options = [
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="character_name",
        description="設定ボイス",
        required=True,
        choices=[
            interactions.Choice(name="さとうささら", value="さとうささら"),
            interactions.Choice(name="すずきつづみ", value="すずきつづみ"),
            ], 
        ),
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="item",
        description="変更箇所",
        required=True,
        choices=[
            interactions.Choice(name="音の大きさ(共通)", value="volume"),
            interactions.Choice(name="話す速さ(共通)", value="speed"),
            interactions.Choice(name="音の高さ(共通)", value="tone"),
            interactions.Choice(name="抑揚(共通)", value="tone_scale"),
            interactions.Choice(name="声質(共通)", value="alpha"),
            interactions.Choice(name="元気(ささら)", value="元気"),
            interactions.Choice(name="普通(ささら)", value="普通"),
            interactions.Choice(name="哀しみ(ささら)", value="哀しみ"),
            interactions.Choice(name="怒り(共通)", value="怒り"),
            interactions.Choice(name="クール(つづみ)", value="クール"),
            interactions.Choice(name="照れ(つづみ)", value="照れ"),
            interactions.Choice(name="喜び(つづみ)", value="喜び"),
            ], 
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="value",
            description="値（0~100）",
            required=True,
        ),
    ],
)
async def cevioai_change_voice_settings(ctx, character_name: str, item: str, value: int):
    try:
        ret = preset.CeVIOAI_change_audio_settings(ctx.author.id, character_name, item, value)
        if ret == 0:
            await ctx.send(F"{character_name}の設定を変更しました", ephemeral=True)
        elif ret == 1:
            await ctx.send(F"変更箇所の値が間違っています", ephemeral=True)
        elif ret == 2:
            await ctx.send(F"変更箇所の値がキャラにあっていません", ephemeral=True)
        return
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\ncharacter_name:{character_name}\nitem{item}\nvalue{value}\n{e}")

# A.I.VOICEボイス設定変更
@inter.command(
    name="aivoice_change_audio_settings",
    description="A.I.VOICEボイス設定変更",
    scope=[server_id],
    options = [
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="character_name",
        description="設定ボイス",
        required=True,
        choices=[
            interactions.Choice(name="栗田まろん", value="栗田まろん"),
            interactions.Choice(name="紅桜ショウガ", value="紅桜ショウガ"),
            ], 
        ),
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="item",
        description="変更箇所",
        required=True,
        choices=[
            interactions.Choice(name="ボリューム (0~200)", value="Volume"),
            interactions.Choice(name="話速 (0~400)", value="Speed"),
            interactions.Choice(name="高さ (0~200)", value="Pitch"),
            interactions.Choice(name="抑揚 (0~200)", value="PitchRange"),
            interactions.Choice(name="喜び (0~100)", value="J"),
            interactions.Choice(name="怒り (0~100)", value="A"),
            interactions.Choice(name="悲しみ (0~100)", value="S"),
            ], 
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="value",
            description="値",
            required=True,
        ),
    ],
)
async def aivoice_change_audio_settings(ctx, character_name: str, item: str, value: int):
    try:
        ret = preset.AIVoice_change_audio_settings(ctx.author.id, character_name, item, value)
        if ret == 0:
            await ctx.send(F"{character_name}の設定を変更しました", ephemeral=True)
        elif ret == 1:
            await ctx.send(F"値が間違っています 0～100までです", ephemeral=True)
        elif ret == 2:
            await ctx.send(F"値が間違っています 0～400までです", ephemeral=True)
        elif ret == 3:
            await ctx.send(F"値が間違っています 0～200までです", ephemeral=True)
        return
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\ncharacter_name:{character_name}\nitem{item}\nvalue{value}\n{e}")

# CCB
@inter.command(
    name="ccb",
    description="CCB",
    scope=server_id,
    options = [
        interactions.Option(
            name="num",
            description="数値",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
    ],
)
async def ccb(ctx, num):
    try:
        await ctx.send(F"CCB<={num}\n{all.CCB(f'CCB<={num}')}")
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\n{e}")

# クリティカル or ファンブル
@inter.command(
    name="c_or_f",
    description="クリティカル or ファンブル",
    scope=server_id,
    options = [
        interactions.Option(
        type=interactions.OptionType.STRING,
        name="setting",
        description="クリティカル or ファンブルの設定ができます",
        required=False,
        choices=[
            interactions.Choice(name="クリティカル", value="critical"),
            interactions.Choice(name="ファンブル", value="fumble")
            ], 
        ),
    ],
)
async def c_or_f(ctx, setting: str = None):
    #print(setting)
    if setting == "critical":
        critical=True
        fumble=False
    elif setting == "fumble":
        critical=False
        fumble=True
    else:
        critical=True
        fumble=True

    try:
        await ctx.send(F"{all.c_or_f(critical, fumble)}")
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\n{e}")

# 日本語に翻訳
@inter.command(
    name="translate_to_japanese",
    description="日本語に翻訳",
    scope=server_id,
    options = [
        interactions.Option(
            name="word",
            description="ワード",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def translate_to_japanese(ctx, word,):
    try:
        retu = DeepLAPI.to_JA(word)
        await ctx.send(F"Before: {word}\n  検出言語: {retu[1]}\nAfter: {retu[0]}")
    except Exception as e:
        await ctx.send(F"エラーが発生しました。\n{e}")


load_settings()
lp = asyncio.get_event_loop()
lp.create_task(bot.start(TOKEN)) #discord.pyを起動
lp.create_task(inter._ready()) #interactions.pyを起動
lp.run_forever()
