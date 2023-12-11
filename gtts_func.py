from gtts import gTTS, lang


class TextToSpeech:
    def __init__(self, language: str):
        self.language = language
    def convert_to_audio(self, text, audio_path):
        audio = gTTS(text=text, lang=self.language, slow=False)
        audio.save(audio_path)
        return audio
def all_language():
    dictionary = lang.tts_langs()
    return dictionary