import os
from transformers import pipeline
from PIL import Image

print("Loading model...")
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

frames = sorted([f for f in os.listdir() if f.endswith(".jpg")])

prev_caption = ""
story = []

def clean_caption(text):
    text = text.replace(" ' s", "'s")
    return text.strip()

def make_sentence(text):
    return text.capitalize() + "."

with open("timestamps.txt", "w") as file:

    for i, frame in enumerate(frames):
        try:
            image = Image.open(frame)
            result = captioner(image)
            caption = clean_caption(result[0]['generated_text'])

            if prev_caption == "" or caption.lower() not in prev_caption.lower():
                time = i * 2
                minutes = time // 60
                seconds = time % 60

                sentence = make_sentence(caption)

                line = f"{minutes:02d}:{seconds:02d} - {sentence}"
                print(line)

                file.write(line + "\n")
                story.append(sentence)

            prev_caption = caption

        except Exception as e:
            print(f"Error: {e}")

# Create story output
with open("story.txt", "w") as f:
    paragraph = " ".join(story)
    f.write(paragraph)

print("\nStory Generated:\n")
print(paragraph)