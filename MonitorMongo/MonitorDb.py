import logging
import json
from pymongo import monitoring,MongoClient,DESCENDING

class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        print("Command {0.command_name} with request id "
                     "{0.request_id} started on server "
                     "{0.connection_id}".format(event))

    def succeeded(self, event):
        print("dir",event._CommandEvent__cmd_name)
        if event._CommandEvent__cmd_name == "insert":
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["mydatabase"]
            mycol = mydb["event"]
            col = mycol.find_one(sort=[( '_id',
             DESCENDING)])
            print("col ",col["name"])


    def failed(self, event):
        print("Command {0.command_name} with request id "
                     "{0.request_id} on server {0.connection_id} "
                     "failed in {0.duration_micros} "
                     "microseconds".format(event))
