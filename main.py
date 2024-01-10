from PIL import Image
from PIL import ImageOps
from roboflow import Roboflow
from dotenv import load_dotenv
import pytesseract
import numpy as np
import cv2
import os
import json
image_frames = 'image_frames'

def getJsonFromRoboflow(image_name):

    load_dotenv("api.env")

    key = os.getenv('API_KEY')

    rf = Roboflow(api_key=key)
    project = rf.workspace().project("detect-chat-dad")
    model = project.version(1).model

    return model.predict("./image_frames/" + image_name, confidence=40, overlap=30).json()

def visualiseFromRoboflow(image_name, predicted_image_name):
    rf = Roboflow(api_key="mnr8bLySCxMb9jLHFl0f")
    project = rf.workspace().project("detect-chat-dad")
    model = project.version(1).model

    model.predict("./image_frames/" + image_name, confidence=40, overlap=30).save(predicted_image_name)


def files():
    try:
        os.remove(image_frames)
    except OSError:
        pass

    if(not os.path.exists(image_frames)):
        os.makedirs(image_frames)
    
    src_vid = cv2.VideoCapture('dad_store_feed.mkv')
    return(src_vid)

def process(src_vid):
    #We're going to capture every 100th frame of the video to keep the amount of images reasonable.
    index = 0
    while src_vid.isOpened():
        ret, frame = src_vid.read()

        #Break when we are done reading
        if not ret:
            break

        name = './image_frames/frame' + str(index) + '.png'

        #name each frame
        if index % 100 == 0:
            print("Extracting frame" + name)
            cv2.imwrite(name, frame)
        
        index += 1

        if(cv2.waitKey(10) & 0xFF == ord('q')):
            break

    src_vid.release()
    cv2.destroyAllWindows()

def old_txt_read():
    filename = 'image_01.png'
    img1 = np.array(Image.open(filename))
    text = pytesseract.image_to_string(img1)

    print(text)

def cropSellerListings(roboJSON, orignal_image):
    clippings = [] # empty array for image clips

    for box in roboJSON["predictions"]:
        img = Image.open("./image_frames/" + orignal_image)
        #This doesn't work, need to understand the rectangles better
        x1 = box["x"] - (box["width"] / 2)
        x2 = box["x"] + (box["width"] / 2)
        y1 = box["y"] - (box["height"] / 2)
        y2 = box["y"] + (box["height"] / 2)

        #test = [x1, x2, y1, y2]
        #print("x1:" + str(test[0]) + "," + "x2:" + str(test[1]) + "," + "y1:" + str(test[2]) + "," + "y2:" + str(test[3]))

        cropped = img.crop((x1, y1, x2, y2))
        clippings.append(cropped)

    return clippings

def saveClipsToFile(clips):
    index = 0

    for clip in clips:
       clip.save("./test_clips/frame100_" + str(index) + "_.png")
       index += 1

def convertClipsToStrings(clips):

    listing_strings = []

    for clip in clips:
        img1 = np.array(clip)
        text = pytesseract.image_to_string(img1)
        listing_strings.append(text)
    
    print(*listing_strings, sep='\n')


if __name__ == '__main__':
   json1 = getJsonFromRoboflow("frame100.png")
   clips = cropSellerListings(json1, "frame100.png")
   convertClipsToStrings(clips)


   
