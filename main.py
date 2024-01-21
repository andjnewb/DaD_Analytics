from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import pytesseract
import numpy as np
import cv2
import os
import json
import time
import pickle
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
image_frames = 'image_frames'

#Weapons strings 
sword_names = ["Arming", "Falchion", "Longsword", "Rapier", "Short", "Viking", "Zweihander"]
mace_names = ["Flanged Mace", "Morning Star", "Torch", "Quarterstaff", "War Maul"]
dagger_names = ["Castillon", "Kris", "Rondel", "Stiletto"]
polearm_names = ["Bardiche", "Halberd", "Spear"]
axe_names = ["Battle", "Double", "Felling", "Hatchet", "Horsemans"]
bow_names = ["Longbow", "Recurve", "Survival"]
crossbow_names = ["Crossbow", "Hand", "Windlass"]
magic_stuff_names = ["Ball", "Sword", "Staff", "Spellbook"]
instrument_names = ["Drum", "Flute", "Lute", "Lyre"]
shield_names = ["Buckler", "Heater", "Pavise", "Round"]


def captureDaDScreenshot(image_name):
    rects = getDisplayRects()
    saveRectToBmp("./image_frames/" + image_name + ".bmp",rects[1])


def getJsonFromRoboflow(image_name):

    load_dotenv("api.env")

    key = os.getenv('API_KEY')


    rf = Roboflow(api_key=key)
    project = rf.workspace().project("detect-chat-dad")
    model = project.version(1).model

    return model.predict("./image_frames/" + image_name + ".bmp", confidence=40, overlap=30).json()


def old_txt_read():
    filename = 'image_01.png'
    img1 = np.array(Image.open(filename))
    text = pytesseract.image_to_string(img1)

    print(text)

def cropSellerListings(roboJSON, orignal_image):
    clippings = [] # empty array for image clips

    for box in roboJSON["predictions"]:
        img = Image.open("./image_frames/" + orignal_image)
        
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

def writeWeaponDataToFile(weapon_maps):

    with open("weapon_data.dat", "wb") as fp:
        pickle.dump(weapon_maps, fp)
        print("Weapon data written to file.")
    
    fp.close()


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
    quit = 0
    image_index = 0
    weapon_maps = initWeaponMaps()
    while(quit == 0):
        time.sleep(1)
        captureDaDScreenshot("image_" + str(image_index))
        
        
        json1 = getJsonFromRoboflow("image_" + str(image_index))
        clips = cropSellerListings(json1, "image_" + str(image_index) + ".bmp")
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
        writeWeaponDataToFile(weapon_maps)
        image_index += 1
        


    
    
    
    
    
    
   
   


   
