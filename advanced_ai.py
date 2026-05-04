import os
from transformers import pipeline
from PIL import Image
from ultralytics import YOLO

print("Loading models...")

# AI Caption model
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Object detection model
detector = YOLO("yolov8n.pt")

frames = sorted([f for f in os.listdir() if f.endswith(".jpg")])

prev_output = ""
story = []

def clean_caption(text):
    return text.replace(" ' s", "'s").strip()

def make_sentence(text):
    return text.capitalize() + "."

print("\nProcessing...\n")

for i, frame in enumerate(frames):
    try:
        image = Image.open(frame)

        # Caption
        result = captioner(image)
        caption = clean_caption(result[0]['generated_text'])

        # Object detection
        results = detector(frame)
        objects = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                name = detector.names[cls]
                objects.append(name)

        objects = list(set(objects))

        # Combine output
        combined = f"{make_sentence(caption)} (Objects: {', '.join(objects)})"

        # Filter duplicates
        if combined != prev_output:
            time = i * 2
            minutes = time // 60
            seconds = time % 60

            line = f"{minutes:02d}:{seconds:02d} - {combined}"
            print(line)

            story.append(make_sentence(caption))

        prev_output = combined

    except Exception as e:
        print(f"Error: {e}")

# Save story
with open("advanced_story.txt", "w") as f:
    paragraph = " ".join(story)
    f.write(paragraph)

print("\nStory:\n")
print(paragraph)