from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def get_buildings(db, u_id):
    result = []
    apartments = db.connect().execute(
        'select m.b_id, m.is_admin,b.country,b.city,b.street,b.number,b.name from management as m ' +
        'LEFT OUTER JOIN buildings as b on m.b_id = b.b_id where m.u_id ="' + u_id + '"').cursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            IS_ADMIN: apartment[1],
            COUNTRY: apartment[2],
            CITY: apartment[3],
            STREET: apartment[4],
            NUMBER: apartment[5],
            NAME: apartment[6],
        })
    return jsonify({DATA: result})


def add_building(db):
    try:
        params = request.get_json()
        if NAME not in params:
            params[NAME] = None
        if COUNTRY in params and CITY in params and STREET in params and NUMBER in params:
            guid = str(uuid.uuid4())
            result = db.connect().execute(
                'INSERT INTO buildings (b_id,country,city,street,number,name) VALUES (%s,%s,%s,%s,%s,%s)',
                (guid, params[COUNTRY], params[CITY], params[STREET], params[NUMBER], params[NAME]))
            if result.rowcount > 0:
                return jsonify({DATA: {BID: guid}})
            else:
                return jsonify({ERROR: ZERO_ROWS_AFFECTED})
        return jsonify({ERROR: WRONG_PARAMETERS})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


def search(db, content):
    result = []
    regex_content = '"%%' + content.replace(' ', '%%') + '%%"'
    query = 'select b_id, name, country, city, street, number from buildings' \
            ' where concat(country,city,street,number,name) like {0}' \
            ' or concat(city,country,street,number,name) like {1}' \
            ' or concat(city,street,country,number,name) like {2}' \
            ' or concat(number,country,city,street,name) like {3}' \
            ' or concat(number,city,street,country,name) like {4}'.format(regex_content, regex_content, regex_content,
                                                                          regex_content, regex_content)
    apartments = db.connect().execute(query).cursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            NAME: apartment[1],
            COUNTRY: apartment[2],
            CITY: apartment[3],
            STREET: apartment[4],
            NUMBER: apartment[5],
        })
    return jsonify({DATA: result})


def is_building_exists(buildings_json, b_id):
    for building in buildings_json:
        if building[BID] == b_id:
            return True
    return False
