import json
import time

file_names = "VoicePreset.json"

default_preset = {
    "VOICE": {
            "character_name": "さとうささら",
            "emotion": {
                "元気": 100,
                "哀しみ": 0,
                "怒り": 0,
                "普通": 0
            },
            "generation_software": "CeVIO AI",
            "setting": {
                "alpha": 50,
                "speed": 50,
                "tone": 50,
                "tone_scale": 50,
                "volume": 50
            }
        },
    "setting_data": {
        "さとうささら": {
            "character_name": "さとうささら",
            "emotion": {
                "元気": 100,
                "哀しみ": 0,
                "怒り": 0,
                "普通": 0
            },
            "generation_software": "CeVIO AI",
            "setting": {
                "alpha": 50,
                "speed": 50,
                "tone": 50,
                "tone_scale": 50,
                "volume": 50
            }
        },
    }
}

preset_list = {
    "さとうささら": "CeVIO AI",
    "すずきつづみ": "CeVIO AI",
    "栗田まろん": "A.I.VOICE",
    "紅桜ショウガ": "A.I.VOICE",
    }

CeVIOAI_setting = {
    "volume":50,        # 音の大きさ
    "speed":50,         # 話す速さ
    "tone":50,          # 音の高さ
    "alpha":50,         # 声質
    "tone_scale":50     # 抑揚
}

sato_sasara_emotion = {
    "元気":100,
    "普通":0,
    "怒り":0,
    "哀しみ":0
}

suzuki_tsudumi_emotion = {
    "クール":100,
    "照れ":0,
    "怒り":0,
    "喜び":0,
    "ひそひそ":0
}

AIVoice_VoiceName_data = {
    "栗田まろん": "KuritaMaron_48",
    "紅桜ショウガ": "BenizakuraSyoga_48"
}

def AIVoice_setting(character_name):
    setting_data = {
        "VoicePreset": {
            "PresetName":character_name,
            "VoiceName":AIVoice_VoiceName_data[character_name],
            #"MergedVoiceContainer":{
                #"BasePitchVoiceName":"",
                #"MergedVoices":[]
            #},
            "Volume":1,
            "Speed":1,
            "Pitch":1,
            "PitchRange":1,
            #"MiddlePause":150,
            #"LongPause":370,
            "Styles":{
                "J":0,
                "A":0,
                "S":0
            }
        },
        "character_name": character_name,
        "generation_software": preset_list[character_name]
    }
    return(setting_data)

def json_open(file_name=file_names):
    with open(file_name, "r", encoding="utf-8_sig") as f:
        json_file = json.load(f)
        return(json_file)

def json_write(data, file_name=file_names):
    with open(file_name, 'w', encoding="utf-8_sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        time.sleep(0.1)

def config_change(key=None, value=None):
    file_name = "configs.json"
    json_file = json_open(file_name)
    if key == None:
        return(json_file)
    
    json_file[str(key)] = value
    json_write(json_file, file_name)

def VoicePreset_json_write(user_id, character_name=None, json_file=None):
    user_id = str(user_id)
    if json_file == None:
        json_file = json_open()

    if user_id not in json_file:
        json_file.update({user_id:default_preset})

    if character_name == None:
        # デフォルト設定書き込み
        weight_dict = {user_id:default_preset}
    else:
        # "setting_data"内に変更キーがある場合
        if character_name in json_file[user_id]["setting_data"]:
            weight_dict = json_file[user_id]["setting_data"][character_name]
            json_file[user_id]["VOICE"] = (weight_dict)

        else:
            weight_dict = {
                user_id: {
                    "VOICE":{
                        "character_name":character_name,
                        "generation_software":preset_list[character_name],
                    },
                    "setting_data":{}
                }
            }

            # CeVIOの初回設定書き込み
            if preset_list[character_name] == "CeVIO AI":
                weight_dict[user_id]["VOICE"]["setting"] = CeVIOAI_setting
                if character_name == "さとうささら":
                    weight_dict[user_id]["VOICE"]["emotion"] = sato_sasara_emotion
                elif character_name == "すずきつづみ":
                    weight_dict[user_id]["VOICE"]["emotion"] = suzuki_tsudumi_emotion
            # A.I.VOICEの初回設定書き込み
            elif preset_list[character_name] == "A.I.VOICE":
                weight_dict[user_id]["VOICE"] = AIVoice_setting(character_name)

            weight_dict[user_id]["setting_data"].update(weight_dict[user_id]["VOICE"])
            json_file[user_id]["setting_data"][character_name]=(weight_dict[user_id]["setting_data"])
            json_file[user_id]["VOICE"].update(weight_dict[user_id]["VOICE"])
    json_write(json_file)
    return(json_file)

def VoicePreset_json_get(user_id):
    json_file = json_open()
    try:
        preset = json_file[str(user_id)]["VOICE"]
    except KeyError:
        VoicePreset_json_write(user_id, None, json_file)
        json_file = json_open()
        preset = json_file[str(user_id)]["VOICE"]
    except Exception as e:
        print("VoicePreset_json_get" + str(e))
    return(preset)


def CeVIOAI_change_audio_settings(user_id, character_name, item, value):
    if 0 <= value <= 100:
        pass
    else:
        return(1)

    if item in CeVIOAI_setting:
        pass
    elif character_name == "さとうささら":
        if item in sato_sasara_emotion:
            pass
        else:
            return(2)
    elif character_name == "すずきつづみ":
        if item in suzuki_tsudumi_emotion:
            pass
        else:
            return(2)

    user_id = str(user_id)
    json_file = json_open()
    # データが存在しなかった場合
    if user_id not in json_file:
        json_file = VoicePreset_json_write(user_id, character_name, json_file)
    elif character_name not in json_file[user_id]["setting_data"]:
        json_file = VoicePreset_json_write(user_id, character_name, json_file)
    
    edited_part = json_file[user_id]["setting_data"][character_name]
    if item in ["alpha", "speed", "tone", "tone_scale", "volume"]:
        edited_part["setting"][item] = value
    else:
        edited_part["emotion"][item] = value
    json_file[user_id]["setting_data"][character_name].update(edited_part)
    json_file[user_id]["VOICE"] = (json_file[user_id]["setting_data"][character_name])
    json_write(json_file)
    return(0)


def AIVoice_change_audio_settings(user_id, character_name, item, value):
    value = value / 100
    user_id = str(user_id)

    json_file = json_open()
    # user_idが存在しなかった場合
    if user_id not in json_file:
        json_file = VoicePreset_json_write(user_id, character_name, json_file)
    # ボイスではなかった場合
    elif character_name not in json_file[user_id]["setting_data"]:
        json_file = VoicePreset_json_write(user_id, character_name, json_file)
    
    edited_part = json_file[user_id]["setting_data"][character_name]["VoicePreset"]
    if item in ["A", "J", "S"]:
        if 0 <= value <= 1:
            edited_part["Styles"][item] = value
        else:
            return(1)
    elif item == "Speed":
        if 0 <= value <= 4:
            edited_part[item] = value
        else:
            return(2)
    else:
        if 0 <= value <= 2:
            edited_part[item] = value
        else:
            return(3)

    json_file[user_id]["setting_data"][character_name]["VoicePreset"].update(edited_part)
    json_file[user_id]["VOICE"] = (json_file[user_id]["setting_data"][character_name])

    json_write(json_file)
    return(0)
