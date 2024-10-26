import sasawrapper

print(F"CeVIOAI {sasawrapper.get_cevioai_version()}")

def create(text, preset_data):
    preset_data_setting = preset_data["setting"]
    preset_data_emotion = preset_data["emotion"]

    re = sasawrapper.output_to_wav(
        text,
        "output.wav",
        cast=preset_data["character_name"],
        volume=preset_data_setting["volume"],
        speed=preset_data_setting["speed"],
        tone=preset_data_setting["tone"],
        tone_scale=preset_data_setting["tone_scale"],
        alpha=preset_data_setting["alpha"],
        emotion={
            "元気":preset_data_emotion.get("元気") or 0, # ささら
            "普通":preset_data_emotion.get("普通") or 0, # ささら
            "怒り":preset_data_emotion.get("怒り") or 0, # ささら,つづみ
            "哀しみ":preset_data_emotion.get("哀しみ") or 0, # ささら
            "クール":preset_data_emotion.get("クール") or 0, # つづみ
            "照れ":preset_data_emotion.get("照れ") or 0, # つづみ
            "喜び":preset_data_emotion.get("喜び") or 0, # つづみ
            "ひそひそ":preset_data_emotion.get("ひそひそ") or 0, # つづみ
        },
    )
    return(re)
