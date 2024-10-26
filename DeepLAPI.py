import requests

API_KEY =  # DeepLのAPIキーを入力してください str

lang_dic = {
    "BG":"ブルガリア語",
    "CS":"チェコ語",
    "DA":"デンマーク語",
    "DE":"ドイツ語",
    "EL":"ギリシャ語",
    "EN":"英語",
    "EN-BG":"イギリス語",
    "EN-US":"アメリカ語",
    "ES":"スペイン語",
    "ET":"エストニア語",
    "FI":"フィンランド語",
    "FR":"フランス語",
    "HU":"ハンガリー語",
    "ID":"インドネシア語",
    "IT":"イタリア語",
    "JA":"日本語",
    "KO":"韓国語",
    "LT":"リトアニア語",
    "LV":"ラトビア語",
    "NB":"ノルウェー語",
    "NL":"オランダ語",
    "PL":"ポーランド語",
    "PT-BR":"ポルトガル語",
    "PT-PT":"ポルトガル語",
    "RO":"ルーマニア語",
    "RU":"ロシア語",
    "SK":"スロバキア語",
    "SL":"スロベニア語",
    "SV":"スウェーデン語",
    "TR":"トルコ語",
    "UK":"ウクライナ語",
    "ZH":"中国語(簡体字)",
}

def main(params):
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)

    result = request.json()

    try:
        detection_lang = lang_dic[F"{result['translations'][0]['detected_source_language']}"]
    except:
        detection_lang = F"言語の検出ができませんでした {result['translations'][0]['detected_source_language']}"

    return([F"{result['translations'][0]['text']}", detection_lang])


def to_JA(text):
    params = {
        "auth_key": API_KEY,
        "text": text,
        "target_lang": "JA" 
        }
    re = main(params)
    return(re)

def to_EN(text):
    params = {
        "auth_key": API_KEY,
        "text": text,
        "target_lang": "EN" 
        }
    re = main(params)
    return(re)

def JA_to_EN(text):
    params = {
        "auth_key": API_KEY,
        "text": text,
        "source_lang": "JA",
        "target_lang": "EN" 
        }
    re = main(params)
    return(re)

def EN_to_JA(text):
    params = {
        "auth_key": API_KEY,
        "text": text,
        "source_lang": "EN",
        "target_lang": "JA" 
        }
    re = main(params)
    return(re)
