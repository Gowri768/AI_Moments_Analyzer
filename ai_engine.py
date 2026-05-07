import os
import cv2
import shutil
import tempfile
from transformers import pipeline
from PIL import Image
from ultralytics import YOLO

print("Initializing AI models...")
# Initialize models globally so they don't reload on every request
try:
    captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    detector = YOLO("yolov8n.pt")
    print("AI models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

def clean_caption(text):
    return text.replace(" ' s", "'s").strip()

def make_sentence(text):
    return text.capitalize() + "."

def extract_frames(video_path, output_dir, frame_interval=60):
    """
    Extracts frames from a video file.
    By default, 60 frames = 2 seconds at 30 fps.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise Exception("Could not open video file.")

    fps = video.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30 # default
        
    # Calculate frames to skip based on 1 frame every 2 seconds
    skip_frames = int(fps * 2)

    frame_count = 0
    saved_count = 0
    frames_paths = []

    while True:
        success, frame = video.read()
        if not success:
            break
        
        if frame_count % skip_frames == 0:
            frame_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            frames_paths.append(frame_path)
            saved_count += 1
        
        frame_count += 1

    video.release()
    return frames_paths

def process_video(video_path):
    """
    Processes a video file and returns a timeline of events and a story.
    """
    temp_dir = tempfile.mkdtemp(prefix="ai_analyzer_")
    
    events = []
    story_sentences = []
    
    try:
        print(f"Extracting frames from {video_path} into {temp_dir}...")
        frame_paths = extract_frames(video_path, temp_dir)
        print(f"Extracted {len(frame_paths)} frames. Processing...")

        prev_output = ""
        
        for i, frame_path in enumerate(frame_paths):
            image = Image.open(frame_path)
            
            # 1. Captioning
            caption_res = captioner(image)
            caption = clean_caption(caption_res[0]['generated_text'])
            sentence = make_sentence(caption)
            
            # 2. Object Detection
            results = detector(frame_path)
            objects = []
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = detector.names[cls]
                    objects.append(name)
            
            objects = list(set(objects)) # unique objects
            
            combined_hash = f"{sentence} (Objects: {', '.join(objects)})"
            
            # Only add if it's new
            if combined_hash != prev_output:
                time_seconds = i * 2
                minutes = time_seconds // 60
                seconds = time_seconds % 60
                time_str = f"{minutes:02d}:{seconds:02d}"
                
                events.append({
                    "time": time_str,
                    "caption": sentence,
                    "objects": objects,
                    "frame_url": "" # We won't send the frames to frontend to keep it simple, or we could. Let's keep it simple.
                })
                story_sentences.append(sentence)
                
            prev_output = combined_hash

    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    paragraph = " ".join(story_sentences)
    return {
        "events": events,
        "story": paragraph
    }
