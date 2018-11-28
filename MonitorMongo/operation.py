from MonitorDb import CommandLogger
from pymongo import monitoring
import pymongo

#monitoring.register(CommandLogger())
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]
mycol = mydb["event"]
col = mycol.save({"name":"pratha"})
print("save",col)
