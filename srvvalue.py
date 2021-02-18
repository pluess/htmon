import os
from flask import Flask
from flask import jsonify
from markupsafe import escape
from pony import orm
from datetime import datetime
import logging
import simplejson as json
from flask import render_template
import dateutil.parser

currentPath = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s', filename=currentPath+'/tempsrv.log')

db = orm.Database()
db.bind(provider='mysql', host='temperatur', user='temperatur_user', passwd='temperatur_password', db='temperaturdb')

class Temperatur(db.Entity):
    zeit = orm.Required(datetime, sql_default='CURRENT_TIMESTAMP')
    t1 = orm.Required(float)
    t2 = orm.Required(float)
    t3 = orm.Required(float)

db.generate_mapping(create_tables=True)
app = Flask(__name__)

@app.route('/temp/<fromd>/<tod>')
def temp(fromd, tod):
    orm.set_sql_debug(True)
    fromDatetime = dateutil.parser.isoparse(fromd)
    toDatetime = dateutil.parser.isoparse(tod)
    logging.debug(fromDatetime)
    logging.debug(toDatetime)
    with orm.db_session():
        tList = orm.select(t for t in Temperatur if t.zeit >= fromDatetime and t.zeit <= toDatetime)[:]
        result = [t.to_dict(exclude='zeit') for t in tList]
        for i in range(len(result)):
            result[i]['zeit'] = tList[i].zeit.isoformat()
        return jsonify(result)

@app.route('/chart')
def hello():
    return render_template('chart.html')

