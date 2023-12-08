import openai
import speech_recognition as sr
# You might need to import other libraries for speech recognition, e.g., speech_recognition, google.cloud.speech, etc.

class SpeechToText:
    def __init__(self, online: bool, language: str, openai_api_key: str):
        self.online = online
        self.language = language
        openai.api_key = openai_api_key

    def record(self, output_file_id: int) -> str:
        if self.online:
            transcript = self.record_online()
        else:
            transcript = self.record_offline()
        return transcript

    def record_online(self) -> str:
        # Example: Using OpenAI API for speech-to-text

        audio_file_url = "gs://your-audio-file-bucket/audio.wav"  # Replace with your audio file URL
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Transcribe the following audio: {audio_file_url}",
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None,
            log_level="info"
        )
        transcript = response.choices[0].text.strip()
        return transcript


    def record_offline(self) -> str:
        # Initialize recognizer class (for recognizing the speech)
        r = sr.Recognizer()

        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source)
            print("Time over, thanks")

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            print("Text: "+r.recognize_google(audio_text))
            return r.recognize_google(audio_text)
        except:
            print("Sorry, I did not get that")
            return ""
        

