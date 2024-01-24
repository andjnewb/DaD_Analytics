from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
from constants import *
import pytesseract
import numpy as np
import os
import time
import pickle
import re
import mysql.connector
from mysql.connector import Error
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

def connectToMySQL(db):

    load_dotenv("api.env")
    user_name = os.getenv('SQL_USER')
    user_password = os.getenv('SQL_PASS')
    host_name = os.getenv('SQL_HOST')

    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd = user_password, database = db)
        print("Connected to database " + db + ".")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def send_update(connection, query, input_data):
    cursor = connection.cursor()

    try:
        cursor.execute(query, input_data)
        connection.commit()
        print("Querry success, updated ")
        print(input_data)
    except Error as err:
        print(f"Error: '{err}'")


def sendDataToMySQL(weapon_maps, price_maps, avg_maps, connection):

   weapon_vol_update = """UPDATE weapons SET weapon_volume = %s WHERE weapon_name = %s"""
   weapon_avg_update = """UPDATE weapons SET weapon_average_price = %s WHERE weapon_name = %s"""

   ind = 0
   for type in weapon_maps:
        for weapon in type:
            #Update volume
            vol_data = (weapon_maps[ind][weapon], weapon)
            send_update(connection, weapon_vol_update, vol_data)
            #Update price
            price_data = (price_maps[ind][weapon], weapon)
            send_update(connection, weapon_avg_update, price_data)
        ind += 1



def calculateAveragePrices(weapon_vol_map, weapon_price_map, avg_maps):

    ind = 0
    for type in weapon_vol_map:
        for weapon in type:
            if weapon_vol_map[ind][weapon] == 0:
                avg_maps[ind][weapon] = 0
            else:
                avg_maps[ind][weapon] = weapon_price_map[ind][weapon] / weapon_vol_map[ind][weapon]
        ind += 1


 



def checkForPrices(listing, price_map):

    #[sword_map, mace_map, dagger_map, polearm_map, axe_map, bow_map, crossbow_map, magicstuff_map, instrument_map, shield_map]
    dagger_map = price_map[2]


    ind = 0
    for type in price_map:
        for weapon in type:
            nameReg = r"\[" + weapon + r"\]"
            nameFound = re.search(nameReg, listing)

            if(nameFound != None):
                print("Found a" + nameFound.group())
                priceFound = re.search(r"[0-9]+.g", listing)

                if(priceFound != None):
                    print("Found a price")
                    #Get rid of anything that isn't a number in the price we found
                    cleaned = ''.join(filter(str.isdigit, priceFound.group()))
                    price_map[ind][weapon] += int(cleaned)
        ind += 1

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

def checkWeaponListingsForVolume(listings, weapon_maps):


    ind = 0

    #How many layers of loops is too evil?
    for listing in listings:
        for type in weapon_maps:
            for weapon in type:
                weapon_maps[ind][weapon] += checkStringForSubstrings(listing, weapon)
            ind += 1
        ind = 0


if __name__ == '__main__':
    quit = 0
    image_index = 0

    #It may seem confusing to initialize volume maps and price maps with the same function, but both price and volume would be the same thing initially, zero.
    #DRY or something
    weapon_maps = initWeaponMaps()
    price_maps = initWeaponMaps()
    avg_maps = initWeaponMaps()
    while(quit == 0):
        #time.sleep(1)
        #captureDaDScreenshot("image_" + str(image_index))
        
        
        #json1 = getJsonFromRoboflow("image_" + str(image_index))
        #clips = cropSellerListings(json1, "image_" + str(image_index) + ".bmp")
        #listings = convertClipsToStrings(clips)


        listings = ["[12:02:09 AM]fantapp: [Longsword] 200g", "[12:02:09 AM]fantapp: [Longsword] 153g", "[12:02:09 AM]fantapp: [Kriss Dagger] 20g"]

        checkWeaponListingsForVolume(listings, weapon_maps)
        
        for listing in listings:
            checkForPrices(listing, price_maps)

        calculateAveragePrices(weapon_maps, price_maps, avg_maps)

        connection = connectToMySQL("DaD_Analytics")
        sendDataToMySQL(weapon_maps, price_maps, avg_maps, connection)
        

        print(price_maps)
        exit()
        #writeWeaponDataToFile(weapon_maps)
        #image_index += 1
        


    
    
    
    
    
    
   
   


   
