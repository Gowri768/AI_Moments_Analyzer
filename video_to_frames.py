import cv2

# Load video
video = cv2.VideoCapture("video.mp4")

frame_count = 0

while True:
    success, frame = video.read()
    
    if not success:
        break
    
    # Save frame every 2 seconds (adjust later)
    if frame_count % 60 == 0:
        cv2.imwrite(f"frame_{frame_count}.jpg", frame)
    
    frame_count += 1

video.release()
print("Frames extracted successfully")