import os
import clr
import json

_editor_dir = os.environ['ProgramW6432'] + '\\AI\\AIVoice\\AIVoiceEditor\\'

if not os.path.isfile(_editor_dir + 'AI.Talk.Editor.Api.dll'):
    print("A.I.VOICE Editor (v1.3.0以降) がインストールされていません。")
    exit()

# pythonnet DLLの読み込み
clr.AddReference(_editor_dir + "AI.Talk.Editor.Api")
from AI.Talk.Editor.Api import TtsControl, HostStatus

tts_control = TtsControl()

# A.I.VOICE Editor APIの初期化
host_name = tts_control.GetAvailableHostNames()[0]
tts_control.Initialize(host_name)

# A.I.VOICE Editorの起動
if tts_control.Status == HostStatus.NotRunning:
    tts_control.StartHost()

def convert_to_JSON(preset_data):
    preset_data_VoicePreset = preset_data["VoicePreset"]
    GetVoicePreset_data = {
        "PresetName":preset_data_VoicePreset["PresetName"],
        "VoiceName":preset_data_VoicePreset["VoiceName"],
        "Volume":preset_data_VoicePreset["Volume"],
        "Speed":preset_data_VoicePreset["Speed"],
        "Pitch":preset_data_VoicePreset["Pitch"],
        "PitchRange":preset_data_VoicePreset["PitchRange"],
        "Styles":[
            {"Name":"J","Value":preset_data_VoicePreset["Styles"]["J"]},     # 喜び（ハイテンション）
            {"Name":"A","Value":preset_data_VoicePreset["Styles"]["A"]},     # 怒り
            {"Name":"S","Value":preset_data_VoicePreset["Styles"]["S"]}      # 悲しみ（ローテンション）
            ]
    }
    return(json.dumps(GetVoicePreset_data))

def create(text, preset_data):
    # A.I.VOICE Editorへ接続
    tts_control.Connect()
    # プリセット設定変更
    tts_control.SetVoicePreset(convert_to_JSON(preset_data))
    # プリセット指定
    tts_control.CurrentVoicePresetName = preset_data["character_name"]
    # テキストを設定
    tts_control.Text = text
    # 保存
    tts_control.SaveAudioToFile("./output.wav",)

    # A.I.VOICE Editorとの接続を終了する
    tts_control.Disconnect()
    return
