import requests
import json
import time
import re
import simpleaudio


def audio_query(text, speaker, max_retry):
    """VOICEVOXに対して音声データ生成用のクエリを発行する。

    Args:
        text (str): 音声データ化するテキスト
        speaker (int): VOICEVOXのキャラクターID
        max_retry (int): 最大リトライ回数

    Raises:
        ConnectionError: リトライ回数超過

    Returns:
        object: query_data
    """
    # 音声合成用のクエリを作成する
    query_payload = {"text": text, "speaker": speaker}
    for query_i in range(max_retry):
        r = requests.post(
            "http://localhost:50021/audio_query",
            params=query_payload,
            timeout=(10.0, 300.0),
        )
        if r.status_code == 200:
            query_data = r.json()
            break
        time.sleep(1)
    else:
        raise ConnectionError(
            "The number of retries has reached the upper limit. audio_query : ",
            "/",
            text[:30],
            r.text,
        )
    return query_data


def synthesis(speaker, query_data, max_retry):
    """音声の合成を行う

    Args:
        speaker (_type_): _description_
        query_data (_type_): _description_
        max_retry (_type_): _description_

    Raises:
        ConnectionError: _description_

    Returns:
        _type_: _description_
    """
    synth_payload = {"speaker": speaker}
    for synth_i in range(max_retry):
        r = requests.post(
            "http://localhost:50021/synthesis",
            params=synth_payload,
            data=json.dumps(query_data),
            timeout=(10.0, 300.0),
        )
        if r.status_code == 200:
            # 音声ファイルを返す
            return r.content
        time.sleep(1)
    else:
        raise ConnectionError(
            "Audio error: Maximum number of retries reached. synthesis : ", r
        )


def text_to_speech(texts, speaker=8, max_retry=20):
    """入力したテキストを音声データに変換する。

    Args:
        texts (str): 音声データ化したいテキスト
        speaker (int, optional): VOICEVOXのキャラクターID Defaults to 8.
        max_retry (int, optional): 最大リトライ回数 Defaults to 20.
    """
    if texts == False:
        # 通信状況が悪い場合を想定。
        texts = "ごめんなさい、うまく聞き取れませんでした。"
    texts = re.split("(?<=！|。|？)", texts)
    play_obj = None
    for text in texts:
        # audio_query
        query_data = audio_query(text, speaker, max_retry)
        # synthesis
        voice_data = synthesis(speaker, query_data, max_retry)
        # 音声の再生
        if play_obj != None and play_obj.is_playing():
            play_obj.wait_done()
        wave_obj = simpleaudio.WaveObject(voice_data, 1, 2, 24000)
        play_obj = wave_obj.play()
