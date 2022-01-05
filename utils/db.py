import json
import os
import sys

import psycopg2

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Database:
    def __init__(self):
        self.db = psycopg2.connect(host=config["database"]["host"], database=config["database"]["database"],
                                   user=config["database"]["user"], port=config["database"]["port"],
                                   password=config["database"]["password"])

    def get_address(self, discord_id):
        cur = self.db.cursor()
        cur.execute(f'select address from public.user where discord_id={discord_id};')
        rtn = cur.fetchone()[0]
        return rtn

    def add_address(self, discord_id, address):
        cur = self.db.cursor()
        cur.execute(f"insert into public.user(discord_id, address) values ({discord_id}, '{address}');")
        self.db.commit()

    def update_address(self, discord_id, address):
        cur = self.db.cursor()
        cur.execute(f"UPDATE public.user SET address='{address}' where discord_id={discord_id};")
        self.db.commit()

    def remove_address(self, discord_id):
        cur = self.db.cursor()
        cur.execute(f"delete from public.user where discord_id={discord_id};")
        self.db.commit()

    def check_if_exists(self, discord_id):
        cur = self.db.cursor()
        cur.execute(f"select * from public.user where discord_id={discord_id};")
        return cur.fetchone()