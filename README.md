## 基本説明
ボイスチャンネルでテキストチャンネルに入力された文字を CeVIOAI AIvoice を利用して音声読み上げをします。<br>

## 必要なソフトウェア
CeVIOAI (さとうささら すずきつづみ)<br>
AIvoice (栗田まろん 紅桜ショウガ)<br>
ffmpeg<br>

## 準備
pip install -r requirements.txt<br>
ffmpegを同一ディレクトリに配置してください。
<https://www.ffmpeg.org/download.html>

<https://discord.com/developers/applications>
からBotを作成してください。<br>
discordbot.pyの該当する箇所にアクセストークンとサーバーID、BOTユーザーIDを入力してください。<br>
DeepLのAPIキーを取得しDeepLAPI.pyの該当する箇所にDeepLのAPIキーを入力してください<br>

## 詳細説明<br>
**Botをボイスチャンネルに接続させる**<br>
ボイスチャンネルに1人目のユーザーが接続すると自動的接続します。<br>
自身がボイスチャンネルに接続中にBotをメンションすることでも接続させることが可能です。<br>

**Botをボイスチャンネルから切断する**<br>
Botが接続中のボイスチャンネルから最後のメンバーが切断すると自動的に切断します。<br>
メンション cutでも切断可能です<br>
