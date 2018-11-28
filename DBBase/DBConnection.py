import pymongo
from pprint import pprint
#from MonitorDb import CommandLogger
from pymongo import monitoring

class DatabaseOperation:
      def __init__(self,database,collection):
        self.myclient= pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS = 10000)
        self.mydb = self.myclient[database]
        self.mycol = self.mydb[collection]

      def save_in_db(self,details):
         self.mycol.save(details)

      def save_or_update(self,query,details):
         self.mycol.update(query,details)

      def retrieve_info(self):
         return self.mycol

      def trigger_db(self,register_class):
          monitoring.register(register_class)
