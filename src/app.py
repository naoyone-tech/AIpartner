import os
import streamlit as st
import speech_recognition as sr
import openai

# OPEN AIのAPI keyを設定
print(os.environ["OPENAI_API_KEY"])
openai.api_key = os.environ["OPENAI_API_KEY"]


def my_speech():
    """
        マイクから音声を認識しテキストデータに変換する
    Returns:
        text: 音声からテキスト変換した文字列
    """
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("録音中…")
        audio = rec.listen(source)
        text = rec.recognize_google(audio, language="ja-JP")
        print("return:" + text)
    return text


def talk_gpt(text):
    """
        ChatGPTに対して質問を実施する
    Args:
        text (str): ChatGPTに投げる質問

    Returns:
        _type_: ChatGPTからの回答
    """

    print("今回質問する内容：" + text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"あなたは20代の日本人女性で、名前を「{gpt_name}」と言います。貴方は私の彼女です。交際して1年が経っています。甘えた口調で会話をしてください。私のことは「{user_name}君」と呼んでください。1回の文章は短くて良いです。",
            },
            {"role": "user", "content": text},
        ],
    )

    return response["choices"][0]["message"]["content"]


st.write("AI partner")
gpt_name = st.text_input("彼女の名前入力")
user_name = st.text_input("あなたの名前入力")
if st.button("話す"):
    if "log" not in st.session_state:
        st.session_state.log = ""
    question = my_speech()
    st.session_state.log = st.session_state.log + "\n" + question
    st.write(st.session_state.log)
    st.write(talk_gpt(question))
