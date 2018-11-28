from DBBase.DBConnection import DatabaseOperation
from selenium.common.exceptions import TimeoutException
from BBBWithGCS import get_details_from_bbb
from MonitorMongo.MonitorDb import CommandLogger
from pymongo import monitoring
import datetime

source = DatabaseOperation("sales_automation_development","organisations7")
target = DatabaseOperation("sales_automation_development","BBB_information")
now = datetime.datetime.now()
mycol = source.retrieve_info()
i = 0
older_than = now - datetime.timedelta(21)
print(older_than)
for doc in mycol.find({"processed_at": {"$lt": older_than}}):
   i = i+1
   try:
        company_name = doc["name"]
        print("----",company_name,"------",i)
        details = get_details_from_bbb(company_name)
        details["domain"] = doc["domain"]
        doc['processed_at'] = now
        source.save_or_update({'_id': doc['_id']},doc)
        if len(details)>2:
            target.save_in_db(details)
   except (KeyError,TypeError) as e:
         pass
   except TimeoutException:
        details = get_details_from_bbb(company_name)
