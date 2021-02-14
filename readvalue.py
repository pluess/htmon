import os
from datetime import datetime
import requests
import logging
from pony import orm

currentPath = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s', filename=currentPath+'/readvalue.log') 

r =requests.get("http://192.168.1.122")
tempvalues = r.json()
logging.info(tempvalues)

#orm.set_sql_debug(True)
db = orm.Database()
db.bind(provider='mysql', host='localhost', user='temperatur_user', passwd='temperatur_password', db='temperaturdb')

class Temperatur(db.Entity):
    zeit = orm.Required(datetime, sql_default='CURRENT_TIMESTAMP')
    t1 = orm.Required(float)
    t2 = orm.Required(float)
    t3 = orm.Required(float)

db.generate_mapping(create_tables=True)

with orm.db_session():
    Temperatur(t1=tempvalues[0], t2=tempvalues[1], t3=tempvalues[2])

