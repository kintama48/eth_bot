import json
import os
import sys

import pymongo

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Database:
    def __init__(self):
        db = pymongo.MongoClient(config['database_url'])['eth_records']
        self.collection = db['users']

    def get_address(self, discord_id):
        return self.collection.find_one({"discordID": str(discord_id)})["address"]

    def check_if_exists(self, discord_id):
        return self.collection.find_one({'discordID': str(discord_id)})
