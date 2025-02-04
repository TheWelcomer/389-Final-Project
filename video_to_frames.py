import cv2
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tqdm import tqdm
from numpy import isnan
import math

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


""" video_path = "labeled/0.hevc"
output_folder = "vid0_frames" """


""" video_to_frames(video_path, output_folder)
print("Frames extracted successfully.") """

def frames_to_video(input_folder, video_path=""):
    imgs = []
    print("Fetching image filenames:")
    for filename in tqdm(os.listdir(input_folder)):
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
    print ("Adding frames to video:")
    for i in tqdm(range(len(imgs))):
        video.write(cv2.imread(imgs[i]))
        #print ("frame ", imgs[i])
    video.release()
    print ("\nVideo released")

def create_labeled_frames(input_folder, text_labels, output_folder, new_filename="", **kwargs):
    imgs = []
    print ("Fetching image filenames:")
    for filename in tqdm(os.listdir(input_folder)):
        img = os.path.join(input_folder, filename)
        if not os.path.isfile(img):
            continue
        imgs.append(filename)
    if not len(imgs) == len(text_labels):
        print (len(imgs), len(text_labels))
        raise AssertionError("Number of images not same as number of labels")

    my_font = ImageFont.truetype("arial.ttf" if not "font" in kwargs else kwargs["font"], 
                                 30 if not "font_size" in kwargs else kwargs["font_size"])

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    print ("Writing new frames:")
    for i in tqdm(range(len(imgs))):
        img = Image.open(os.path.join(input_folder, imgs[i]))
        draw = ImageDraw.Draw(img)
        draw.text((100, 100) if not "position" in kwargs else kwargs["position"], 
                  text_labels[i], align="center", font=my_font, fill=(255, 0, 0) if not "color" in kwargs else kwargs["color"])
        img.save(os.path.join(output_folder, new_filename + imgs[i]))
    print ("\nFinished writing frames")

def create_arrow_frames(input_folder, labels, output_folder, new_filename="", bias=(0, 0), **kwargs):
    imgs = []
    print ("Fetching image filenames:")
    for filename in tqdm(os.listdir(input_folder)):
        img = os.path.join(input_folder, filename)
        if not os.path.isfile(img):
            continue
        imgs.append(filename)
    if not len(imgs) == len(labels):
        print (len(imgs), len(labels))
        raise AssertionError("Number of images not same as number of labels")
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    print ("Adding arrows:")
    for i in tqdm(range(len(imgs))):
        img = Image.open(os.path.join(input_folder, imgs[i]))
        draw = ImageDraw.Draw(img)
        add_arrow(draw, labels[i][0], labels[i][1], (img.width/2, img.height-200), bias[0], bias[1])
        img.save(os.path.join(output_folder, new_filename + imgs[i]))
    
    print("\nFinished adding arrows")

def add_arrow(img_d, pitch, yaw, center, pitch_bias=0, yaw_bias=0):
    if isnan(pitch) or isnan(yaw):
        return
    length = 50*((pitch+pitch_bias) * 180 / math.pi)
    start = center
    x_degrees = math.sin(yaw)+yaw_bias

    end = (center[0] + 10*x_degrees*length, center[1] - math.cos(yaw)*length)
    arrow_width = 10
    #print (length, start, end)

    img_d.line([start, end], fill="red", width=arrow_width)

""" labels = []
with open("./labeled/0.txt") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        data = line.split(" ")
        new_label = "Pitch: " + data[0] + ", yaw: " + data[1]
        labels.append(new_label)
create_labeled_frames("./vid0_frames", labels, "./vid0_labeled")
frames_to_video("./vid0_labeled", "./videos/vid0_arrows.mp4") """

biases = [-3.12e-02, -.95e-02, -4.95e-02, -1.95e-02, -5.4e-02]

""" for i in []:
    labels_file = "./labeled/" + str(i) + ".txt"
    output_folder = "./vid" + str(i) + "_arrows"
    frames_folder = "./vid" + str(i) + "_labeled"
    output_file = "./videos/video" + str(i) + "_arrows.mp4"
    labels = []
    with open(labels_file) as f:
        lines = f.readlines()
        for j, line in enumerate(lines):
            data = line.split(" ")
            new_label = [float(data[0]), float(data[1])]
            labels.append(new_label)
    create_arrow_frames(frames_folder, labels, output_folder, bias=(0, biases[i]))
    frames_to_video(output_folder, output_file)

for i in range(5, 10):
    frames_folder = "./vid" + str(i) + "_frames"
    video_path = "./videos/vid" + str(i) + ".mp4"
    frames_to_video(frames_folder, video_path) """