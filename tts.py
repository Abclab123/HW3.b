from gtts import gTTS


class TextToSpeech:
    def __init__(self, language: str):
        self.language = language

    def convert_to_audio(self, text, file_id: int):
        audio = gTTS(text=text, lang=self.language, slow=False)
        audio.save(f"{file_id}.mp3")


if __name__ == "__main__":
    text0 = """
    Once upon a time, in a quaint village nestled between rolling hills, there lived a curious young girl named Lily. She had sparkling blue eyes and a heart full of dreams. One day, as she wandered into the enchanted forest near her home, she discovered a magical talking rabbit named Oliver.
    """
    text1 = """
    山洞住了一隻小熊，而熊爺爺看小熊總是很羨慕朋友有小木屋可以住，某天便說：「你去造間小木屋住吧！」就這樣，小熊在春天時走進森林，牠看見了樹上長滿了綠葉而捨不得砍；到了夏天，小熊又走進了森林，此時樹上開滿了花朵，小熊看見這樣的美景便捨不得砍下樹頭。到了秋天，小熊再次走進，看見樹上掛滿了一顆顆果實，還是捨不得砍下。
    """
    text2 = """
    NTU COOL 在 2022 年 9 月取代 CEIBA 的角色，正式成為本校主要的教學平臺。除了盡力維持系統運作順暢外，我們亦致力於爲NTU COOL開發新功能，或串接外部工具，以盡可能貼近臺大師生的使用期待，如自行開發的影片功能、語音辨識、成績管理；串接Tunritin 和 Gradescope 等工具。
    """
    tts_en = TextToSpeech("en")
    tts_en.convert_to_audio(text0, 0)

    tts_zh_TW = TextToSpeech("zh-TW")
    tts_zh_TW.convert_to_audio(text1, 1)
    tts_zh_TW.convert_to_audio(text2, 2)
