import pymongo

db = pymongo.MongoClient("mongodb+srv://eth_bot:eth_pass"
                                          "@cluster0.rertq.mongodb.net/eth_records?retryWrites=true&w=majority")['eth_records']
collection = db['users']

dummy_data = {"discordID": '123', "address": "https://fourchan"}


def check(discord_id):
    return collection.find_one({'discordID': str(discord_id)})


if not check('123'):
    print("inside")
    collection.insert_one(dummy_data)

print(collection.find_one({"discordID": '123'}))
# print(collection.delete_one({"discordID": 123}))
# print(collection.find_one({"discordID": 123}))




