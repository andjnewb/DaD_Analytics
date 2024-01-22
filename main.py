from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import pytesseract
import numpy as np
import os
import time
import pickle
import re
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
image_frames = 'image_frames'


#Weapons strings 
sword_names = ["Arming Sword", "Falchion", "Longsword", "Rapier", "Short Sword", "Viking Sword", "Zweihander"]
mace_names = ["Flanged Mace", "Morning Star", "Torch", "Quarterstaff", "War Maul"]
dagger_names = ["Castillon Dagger", "Kriss Dagger", "Rondel Dagger", "Stiletto Dagger"]
polearm_names = ["Bardiche", "Halberd", "Spear"]
axe_names = ["Battle Axe", "Double Axe", "Felling Axe", "Hatchet", "Horsemans Axe"]
bow_names = ["Longbow", "Recurve Bow", "Survival Bow"]
crossbow_names = ["Crossbow", "Hand Crossbow", "Windlass Crossbow"]
magic_stuff_names = ["Crystal Ball", "Crystal Sword", "Magic Staff", "Spellbook"]
instrument_names = ["Drum", "Flute", "Lute", "Lyre"]
shield_names = ["Buckler", "Heater Shield", "Pavise", "Round Shield"]

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
        sword_map[sword] += checkStringForSubstrings(listing, sword)

def checkForMaces(listing, mace_map):
    #create map for number of each mace
    
    for mace in mace_map:
        mace_map[mace] += checkStringForSubstrings(listing, mace)    

def checkForDaggers(listing, dagger_map):
    #create map for number of each dagger
    
    for dagger in dagger_map:
        dagger_map[dagger] += checkStringForSubstrings(listing, dagger)

def checkForPolearms(listing, polearm_map):
    #create map for number of each sword
    
    for polearm in polearm_map:
        polearm_map[polearm] += checkStringForSubstrings(listing, polearm)

def checkForAxes(listing, axe_map):
    #create map for number of each sword
    
    for axe in axe_map:
        axe_map[axe] += checkStringForSubstrings(listing, axe)

def checkForBows(listing, bow_map):
    #create map for number of each sword
    
    for bow in bow_map:
        bow_map[bow] += checkStringForSubstrings(listing, bow)

def checkForCrossbows(listing, crossbow_map):
    #create map for number of each sword
    
    for crossbow in crossbow_map:
        crossbow_map[crossbow] += checkStringForSubstrings(listing, crossbow)

def checkForMagicStuff(listing, magicstuff_map):
    #create map for number of each sword
    
    for magicitem in magicstuff_map:
        magicstuff_map[magicitem] += checkStringForSubstrings(listing, magicitem)

def checkForInstruments(listing, instrument_map):
    #create map for number of each sword
    
    for instrument in instrument_map:
        instrument_map[instrument] += checkStringForSubstrings(listing, instrument)

def checkForShields(listing, shield_map):
    #create map for number of each sword
    
    for shield in shield_map:
        shield_map[shield] += checkStringForSubstrings(listing, shield)

def checkForPrices(listing, price_map):

    #[sword_map, mace_map, dagger_map, polearm_map, axe_map, bow_map, crossbow_map, magicstuff_map, instrument_map, shield_map]
    dagger_map = price_map[2]


    for dagger in dagger_map:
        nameReg = r"\[" + dagger + r"\]"
        nameFound = re.search(nameReg, listing)

        if(nameFound != None):
            print("Found a" + nameFound.group())
            priceFound = re.search(r"[0-9]+.g", listing)

            if(priceFound != None):
                print("Found a price")
                #Get rid of anything that isn't a number in the price we found
                cleaned = ''.join(filter(str.isdigit, priceFound.group()))
                dagger_map["Kriss Dagger"] = int(cleaned)




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

def checkStringForSubstrings(string, substring):
    return string.count(substring)

def checkWeaponListingsForVolume(listings):
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



if __name__ == '__main__':
    quit = 0
    image_index = 0

    #It may seem confusing to initialize volume maps and price maps with the same function, but both price and volume would be the same thing initially, zero.
    #DRY or something
    weapon_maps = initWeaponMaps()
    price_maps = initWeaponMaps()
    while(quit == 0):
        #time.sleep(1)
        #captureDaDScreenshot("image_" + str(image_index))
        
        
        #json1 = getJsonFromRoboflow("image_" + str(image_index))
        #clips = cropSellerListings(json1, "image_" + str(image_index) + ".bmp")
        #listings = convertClipsToStrings(clips)

        #checkWeaponListingsForVolume(listings)
        checkForPrices("[12:02:09 AM]fantapp: [Kriss Dagger] 200g", price_maps)
        print(price_maps)
        exit()
        #writeWeaponDataToFile(weapon_maps)
        #image_index += 1
        


    
    
    
    
    
    
   
   


   
