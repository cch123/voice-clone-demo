from TTS.api import TTS

# Example voice cloning with YourTTS in English, French and Portuguese:
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=True)
tts.tts_to_file("this is a new day, so welcome our new friend mario, thank you very much for coming.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
