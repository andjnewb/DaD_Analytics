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

#Weapons strings 
sword_names = ["Arming Sword", "Falchion", "Longsword", "Rapier", "Short Sword", "Viking Sword", "Zweihander"]
mace_names = ["Flanged Mace", "Morning Star", "Torch", "Quarterstaff", "War Maul"]
dagger_names = ["Castillon Dagger", "Kris Dagger", "Rondel Dagger", "Stiletto Dagger"]
polearm_names = ["Bardiche", "Halberd", "Spear"]
axe_names = ["Battle Axe", "Double Axe", "Felling Axe", "Hatchet", "Horsemans Axe"]
bow_names = ["Longbow", "Recurve Bow", "Survival Bow"]
crossbow_names = ["Crossbow", "Hand Crossbow", "Windlass Crossbow"]
magic_stuff_names = ["Crystal Ball", "Crystal Sword", "Magic Staff", "Spellbook"]
instrument_names = ["Drum", "Flute", "Lute", "Lyre"]
shield_names = ["Buckler", "Heater Shield", "Pavise", "Round Shield"]


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
    
    return listing_strings

def checkForSwords(listing, sword_map):
    #create map for number of each sword
    
    for sword in sword_map:
        sword_map[sword] += checkStringForSubtrings(listing, sword)

def checkForMaces(listing, mace_map):
    #create map for number of each mace
    
    for mace in mace_map:
        mace_map[mace] += checkStringForSubtrings(listing, mace)    

def checkForDaggers(listing, dagger_map):
    #create map for number of each dagger
    
    for dagger in dagger_map:
        dagger_map[dagger] += checkStringForSubtrings(listing, dagger)

def checkForPolearms(listing, polearm_map):
    #create map for number of each sword
    
    for polearm in polearm_map:
        polearm_map[polearm] += checkStringForSubtrings(listing, polearm)

def checkForAxes(listing, axe_map):
    #create map for number of each sword
    
    for axe in axe_map:
        axe_map[axe] += checkStringForSubtrings(listing, axe)

def checkForBows(listing, bow_map):
    #create map for number of each sword
    
    for bow in bow_map:
        bow_map[bow] += checkStringForSubtrings(listing, bow)

def checkForCrossbows(listing, crossbow_map):
    #create map for number of each sword
    
    for crossbow in crossbow_map:
        crossbow_map[crossbow] += checkStringForSubtrings(listing, crossbow)

def checkForMagicStuff(listing, magicstuff_map):
    #create map for number of each sword
    
    for magicitem in magicstuff_map:
        magicstuff_map[magicitem] += checkStringForSubtrings(listing, magicitem)

def checkForInstruments(listing, instrument_map):
    #create map for number of each sword
    
    for instrument in instrument_map:
        instrument_map[instrument] += checkStringForSubtrings(listing, instrument)

def checkForShields(listing, shield_map):
    #create map for number of each sword
    
    for shield in shield_map:
        shield_map[shield] += checkStringForSubtrings(listing, shield)


def initWeaponMaps():
    sword_map = {}
    mace_map = {}
    dagger_map = {}
    polearm_map = {}
    axe_map = {}
    bow_map = {}
    crossbow_map = {}
    magicstuff_map = {}
    instrument_map = {}
    shield_map = {}

    for sword in sword_names:
        sword_map[sword] = 0
    for mace in mace_names:
        mace_map[mace] = 0
    for dagger in dagger_names:
        dagger_map[dagger] = 0
    for polearm in polearm_names:
        polearm_map[polearm] = 0
    for axe in axe_names:
        axe_map[axe] = 0
    for bow in bow_names:
        bow_map[bow] = 0
    for crossbow in crossbow_names:
        crossbow_map[crossbow] = 0
    for magicitem in magic_stuff_names:
        magicstuff_map[magicitem] = 0
    for instrument in instrument_names:
        instrument_map[instrument] = 0
    for shield in shield_names:
        shield_map[shield] = 0
    
    return [sword_map, mace_map, dagger_map, polearm_map, axe_map, bow_map, crossbow_map, magicstuff_map, instrument_map, shield_map]

def checkStringForSubtrings(string, substring):
    return string.count(substring)


if __name__ == '__main__':
    weapon_maps = initWeaponMaps()

    json1 = getJsonFromRoboflow("frame100.png")
    clips = cropSellerListings(json1, "frame100.png")
    listings = convertClipsToStrings(clips)

    for listing in listings:
        checkForSwords(listing, weapon_maps[0])
        checkForMaces(listing, weapon_maps[1])
        checkForDaggers(listing, weapon_maps[2])
        checkForPolearms(listing, weapon_maps[3])
        checkForAxes(listing, weapon_maps[4])
        checkForBows(listing, weapon_maps[5])
        checkForCrossbows(listing, weapon_maps[6])
        checkForMagicStuff(listing, weapon_maps[7])
        checkForInstruments(listing, weapon_maps[8])
        checkForShields(listing, weapon_maps[9])

    print(weapon_maps)

   
   


   
