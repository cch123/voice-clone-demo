from TTS.api import TTS

model_name = TTS.list_models()[0]

print("Selected model: ", model_name)

tts = TTS(model_name)

wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])

tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")


# Example voice cloning with YourTTS in English, French and Portuguese:
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=True)
tts.tts_to_file("this is a new day, so welcome our new friend mario, thank you very much for coming.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
