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


video_path = "labeled/0.hevc"
output_folder = "vid0_frames"


""" video_to_frames(video_path, output_folder)
print("Frames extracted successfully.") """

def frames_to_video(input_folder, video_path=""):
    imgs = []
    for filename in os.listdir(input_folder):
        img = os.path.join(input_folder, filename)
        if not os.path.isfile(img):
            continue
        imgs.append(img)
    
    cv2_fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    frame = cv2.imread(imgs[0])
    size = list(frame.shape)
    del size[2]
    size = size[::-1]
    print (size)

    video = cv2.VideoWriter(video_path, cv2_fourcc, 20, size)
    for i in range(len(imgs)):
        video.write(cv2.imread(imgs[i]))
        #print ("frame ", imgs[i])
    video.release()

#frames_to_video("./vid0_frames", "./videos/test1.mp4")