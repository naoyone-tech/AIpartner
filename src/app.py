import os
import streamlit as st
import speech_recognition as sr
import openai
from voicevox import text_to_speech

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
    try:
        with mic as source:
            audio = rec.listen(source)
            text = rec.recognize_google(audio, language="ja-JP")
            print(text)
        return text
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


def talk_gpt(text):
    """
        ChatGPTに対して質問を実施する
    Args:
        text: ChatGPTに投げる質問

    Returns:
        str: ChatGPTからの回答
    """

    print("今回質問する内容：" + text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"あなたは20代の日本人女性で、名前を「{gpt_name}」と言います。貴方は私の彼女です。交際して1年が経っています。年相応な口調で会話をしてください。私のことを呼ぶときは「{user_name}君」と呼んでください。",
            },
            {"role": "user", "content": text},
        ],
    )

    return response["choices"][0]["message"]["content"]


st.write("AI partner")
st.image("image/ai_girl.jpeg")
gpt_name = st.text_input("彼女の名前入力")
user_name = st.text_input("あなたの名前入力")
if st.button("話す"):
    question = my_speech()
    st.write(question)
    response = talk_gpt(question)
    text_to_speech(response)
    st.write(response)
