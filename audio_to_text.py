import whisper

model = whisper.load_model("base")

result = model.transcribe("video4.mp4")

print("\nAudio Text:\n")
print(result["text"])