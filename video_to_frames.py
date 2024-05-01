import cv2
import os

def video_to_frames(video_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    # Read each frame and save it as an image
    while success:
        frame_filename = os.path.join(output_folder, f"frame_{count:04d}.png")  # Save as JPEG images
        cv2.imwrite(frame_filename, image)  # Write the frame as an image file
        success, image = vidcap.read()
        count += 1

    vidcap.release()


video_path = "labeled/1.hevc"
output_folder = "vid1_frames"

video_to_frames(video_path, output_folder)
print("Frames extracted successfully.")
