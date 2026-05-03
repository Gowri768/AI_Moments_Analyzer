import os
from transformers import pipeline
from PIL import Image

# Load AI model (loads once)
print("Loading AI model...")
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Get all frame images and sort them
frames = sorted([f for f in os.listdir() if f.endswith(".jpg")])

print("Processing frames...\n")

prev_caption = ""

for i, frame in enumerate(frames):
    try:
        # Load image
        image = Image.open(frame)

        # Generate caption
        result = captioner(image)
        caption = result[0]['generated_text']

        # Remove duplicate captions
        if caption != prev_caption:
            time = i * 2  # assuming 1 frame every 2 seconds

            minutes = time // 60
            seconds = time % 60

            print(f"{minutes:02d}:{seconds:02d} - {caption}")

        prev_caption = caption

    except Exception as e:
        print(f"Error processing {frame}: {e}")

print("\nDone 🎉")