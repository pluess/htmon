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

@app.route('/temp/<fromd>/<tod>/<samples>')
def temp(fromd, tod, samples):
    orm.set_sql_debug(True)
    fromDatetime = dateutil.parser.isoparse(fromd)
    toDatetime = dateutil.parser.isoparse(tod)
    logging.debug('fromDatetime=%s', fromDatetime)
    logging.debug('toDatetime=%s', toDatetime)
    with orm.db_session():
        tList = orm.select(t for t in Temperatur if t.zeit >= fromDatetime and t.zeit <= toDatetime)[:]
        logging.debug('len(tList)=%d', len(tList))
        sampleStep = int(len(tList) / int(samples))
        logging.debug('sampleStep=%d', sampleStep)
        i = 0
        result = []
        while i<len(tList):
            r = tList[i].to_dict(exclude='zeit')
            r['zeit'] = tList[i].zeit.isoformat()
            result.append(r)
            i += sampleStep
        logging.debug('len(result)=%d', len(result))
        return jsonify(result)

"""         result = [t.to_dict(exclude='zeit') for t in tList]
        for i in range(len(result)):
            result[i]['zeit'] = tList[i].zeit.isoformat()
             return jsonify(result)
"""        

@app.route('/chart')
def hello():
    return render_template('chart.html')

