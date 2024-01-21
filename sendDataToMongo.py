from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import pickle
import os

def sendWeaponVolumeToMongo():

    weapon_file = open("weapon_data.dat", 'rb')
    weapons = pickle.load(weapon_file)

    load_dotenv("api.env")
    username = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASS')

    uri = "mongodb+srv://"+ username + ":" + password + "@dad1.ks3ysrr.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api = ServerApi('1'))

    db = client.Dad1

    weps = db["weapons_volume_db"]


    filter = { }
    try:
        result = weps.insert_many(weapons)
    except MongoClient.errors.OperationFailure:
        print("Error inserting data.")
    
    weapon_file.close()


if __name__ == '__main__':
    sendWeaponVolumeToMongo()