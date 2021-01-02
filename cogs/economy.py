import discord
from discord.ext import commands
import pymongo
import os
import dotenv

from dotenv.main import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_url = os.getenv('mongo_url')
db_client = MongoClient(mongo_url)
db = db_client.get_database('hokage-base')


class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Roast cog is ready')

    async def update_data(user):
        '''
        This Updates the user data in the db to add entry for new members
        '''
        if str(user.guild.id) not in db.list_collection_names():
            server = db[str(user.guild.id)]
            server.insert_one({'server_name': user.guild.name,
                               'server_id': user.guild.id})
            server.insert_one({'id': user.id, 'experience': 0,
                               'level': 0, 'credits': 0, 'kageLevel': 0})
            print(f'{user.guild.name} : {user.guild.id} added to database')
            print(f'{user.id} added to database...')
        else:
            server = db[str(user.guild.id)]
            # print(list(server.find({'id':user.id}))[-1].values())
            try:
                if len(list(server.find({'id': user.id}))) == 0:
                    server.insert_one(
                        {'id': user.id, 'experience': 0, 'level': 0, 'credits': 0, 'kageLevel': 0})
                    print(f'{user.id} added to database')
                elif user.id not in list(server.find({'id': user.id}))[-1].values():
                    server.insert_one(
                        {'id': user.id, 'experience': 0, 'level': 0, 'credits': 0, 'kageLevel': 0})
                    print(f'{user.id} added to database')
            except BaseException:
                print('Some error occured')


def setup(bot):
    bot.add_cog(economy(bot))
