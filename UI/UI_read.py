import streamlit as st


def UI_read(audio_path: str) -> None:
    """UI for reading aloud the generated text.

    Args:
        texts (Dict[str, str]): A dictionary of texts and their corresponding audio paths.

    Returns:
        None
    """

    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")
    except:
        st.error("Error: Audio file not found.")


if __name__ == "__main__":
    gen_results = {
        "TTSMaker是一款免費的文本轉語音工具，提供語音合成服務，支持多種語言，包括英語、法語、德語、西班牙語、阿拉伯語、中文、日語、韓語、越南語等，以及多種語音風格。您可以用它大聲朗讀文本和電子書，或下載音頻文件用於商業用途（完全免費）。作為一款優秀的免費 TTS 工具，TTSMaker 可以輕鬆地將文本在線轉換為語音。": "audios/1.mp3",
        "謹此通知有關我們專案的 UI package 的經過各組決定統一使用 Streamlit 來完成 UI package。同時，我們也稍微調整了 UI 組的截止日期。UI 組的新截止日期將為本週日凌晨 12:00 am。": "audios/2.mp3",
        "我們將會在這個專案中使用 Streamlit 來完成 UI package。": "audios/3.mp3",
    }

    for text, audio_path in gen_results.items():
        st.write(text)
        UI_read(audio_path)
