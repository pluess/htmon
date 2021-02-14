import os
from flask import Flask
from flask import jsonify
from markupsafe import escape
from pony import orm
from datetime import datetime
import logging
import simplejson as json
from flask import render_template

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

@app.route('/temp/<number>')
def temp(number):
    with orm.db_session():
        tList = orm.select(t for t in Temperatur)[:int(number)]
        result = [t.to_dict() for t in tList]
        return jsonify(result)

@app.route('/chart')
def hello():
    return render_template('chart.html')

