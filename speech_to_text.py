import openai
from faster_whisper import WhisperModel
import os

class speech_to_text:
    def __init__(self, online: bool, language: str):
        self.online = online
        self.language = language

    def record(self, output_file_id: int) -> str:
        input_audio = str(output_file_id) + ".mp3"
        if self.online:
            openai.api_key = os.getenv("OPENAI_API_KEY")

            audio_file = open(input_audio, "rb")
            transcript = openai.audio.transcriptions.create(
            model="whisper-1", 
            language=self.language,
            file=audio_file, 
            response_format="text"
            )
            output_list = transcript.split(" ")
            result_str = '. '.join(output_list)
            return result_str
            
        else:
            model_size = "large-v2"
            try:
                model = WhisperModel(model_size, device="cuda", compute_type="float16")
            except:
                model = WhisperModel(model_size, device="cpu", compute_type="float16")
            segments, _ = model.transcribe(input_audio, language = self.language, beam_size=5)

            output_list = []
            for segment in segments:
                output_list.append(segment.text)
            result_str = '. '.join(output_list)
            return result_str