from transformers import pipeline
from PIL import Image

# Load image
image = Image.open("test.png")   # or test.jpg

# Load AI model
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Generate caption
result = captioner(image)

# Print result
print(result[0]['generated_text'])