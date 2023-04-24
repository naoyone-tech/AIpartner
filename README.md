# AIpartner
ChatGPTを用いたAIと会話するプロダクトです。

## ChatGPT
実行するためにはOPEN AIのAPI KEYが必要です。
API KEYを入手後、環境変数OPENAI_API_KEYに登録してください。
https://openai.com/blog/chatgpt

## VOICEVOX
本アプリは音声再生にVOICEVOXを使用しています。
https://voicevox.hiroshiba.jp
上記URLからVOICEVOXのクライアントをインストールするか、
docker-compose upを実行してください。

## image
パートナーとする画像を用意してください。
リポジトリに登録している画像は、Stable DiffusionのPlaygroundで作成した画像になります。
https://stablediffusionweb.com/#demo

## 使用するライブラリ
pip install streamlit
pip install speech_recognition
pip install PyAudio
pip install openai
pip install simpleaudio

## 以下はPyAudioのインストールに必要です。
brew install portaudio

## 開発環境
MacBook Pro()

## 実行方法
以下のコマンドを実行してください。
streamlit run src/app.py

実行後、名前を入力後、「話す」ボタンを押すと会話が始まります。
