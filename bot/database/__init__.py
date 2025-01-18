# -*- coding: utf-8 -*-

from motor.motor_asyncio import AsyncIOMotorClient
from bot import DATABASE_URI, DATABASENAME 

client = AsyncIOMotorClient(DATABASE_URI)

DB = client[DATABASENAME]

async def initdb():
    return DB



