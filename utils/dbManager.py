import json
from motor import motor_asyncio


with open("config/dbconf.json") as f:
    config = json.load(f)


class DBManager:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(config["MONGO_URI"])
        self.db = self.client[config["DB_NAME"]]
        self.GuildConfigCollection = self.db[config["GUILD_CONFIG_COLLECTION_NAME"]]
        self.UserConfigCollection = self.db[config["USER_CONFIG_COLLECTION_NAME"]]

    async def GuildConfigfind(self, query: dict):
        try:
            tryFind = await self.GuildConfigCollection.find_one(query)

            if tryFind:
                data = {}
                for key, value in tryFind.items():
                    data[key] = value
                return data
            else:
                return None
        except Exception as error:
            raise error

    async def GuildConfigdoesExist(self, query: dict):
        try:
            tryFind = await self.GuildConfigCollection.find_one(query)

            if tryFind:
                return True
            else:
                return False
        except Exception as error:
            raise error

    async def GuildConfiginsert(self, data: dict):
        try:
            await self.GuildConfigCollection.insert_one(data)
        except Exception as error:
            raise error

    async def GuildConfigupdate(self, query: dict, data: dict):
        try:
            await self.GuildConfigCollection.update_one(query, {"$set": data})
        except Exception as error:
            raise error

    async def GuildConfigdelete(self, query: dict):
        try:
            await self.GuildConfigCollection.delete_one(query)
        except Exception as error:
            raise error

    async def findUserWarn(self, query: dict):
        try:
            tryFind = await self.UserConfigCollection.find_one(query)

            if tryFind:
                return tryFind["warns"]
            else:
                return None
        except Exception as error:
            raise error

    async def addUserWarn(self, query: dict):
        try:
            findRecords = await self.findUserWarn(query)
            if findRecords:
                await self.UserConfigCollection.update_one(
                    query, {"$set": {"warns": findRecords + 1}}
                )
                return True
            else:
                await self.UserConfigCollection.insert_one(
                    {"guildid": query["guildid"], "userid": query["userid"], "warns": 1}
                )
                return True
        except Exception as error:
            raise error

    async def removeUserWarn(self, query: dict):
        try:
            findRecords = await self.findUserWarn(query)
            if findRecords:
                await self.UserConfigCollection.update_one(
                    query, {"$set": {"warns": findRecords - 1}}
                )
                return True
            else:
                return False
        except Exception as error:
            raise error

    async def updateUserWarn(self, query: dict, data: dict):
        try:
            await self.UserConfigCollection.update_one(query, {"$set": data})
            return True
        except Exception as error:
            raise error
