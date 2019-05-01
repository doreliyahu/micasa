from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def get_buildings(cursor, u_id):
    result = []
    cursor.execute('select m.b_id, m.is_admin,b.country,b.city,b.street,b.number from management as m ' +
                   'LEFT OUTER JOIN buildings as b on m.b_id = b.b_id where m.u_id =' + u_id)
    apartments = cursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            IS_ADMIN: apartment[1],
            COUNTRY: apartment[2],
            CITY: apartment[3],
            STREET: apartment[4],
            NUMBER: apartment[5],
        })
    return jsonify({DATA: result})


def add_building(db):
    try:
        params = request.get_json()
        if NAME not in params:
            params[NAME] = None
        if COUNTRY in params and CITY in params and STREET in params and NUMBER in params:
            guid = str(uuid.uuid4())
            db.cursor().execute('INSERT INTO buildings (b_id,country,city,street,number,name) VALUES (%s,%s,%s,%s,%s,%s)',
                             (guid,params[COUNTRY], params[CITY], params[STREET], params[NUMBER], params[NAME]))
            db.commit()
            return jsonify({DATA: {"b_id": guid}})
        return jsonify({ERROR: "wrong parameters"})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


def search(cursor, content):
    result = []
    regex_content = '"%' + content.replace(' ', '%') + '%"'
    query = 'select b_id, name, country, city, street, number from  buildings' \
            ' where concat(country,city,street,number,name) like ' + regex_content + \
            ' or concat(city,country,street,number,name) like ' + regex_content + \
            ' or concat(city,street,country,number,name) like ' + regex_content + \
            ' or concat(number,country,city,street,name) like ' + regex_content + \
            ' or concat(number,city,street,country,name) like ' + regex_content
    cursor.execute(query)
    apartments = cursor.fetchall()
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


def is_building_exists(buildings_json,b_id):
    for building in buildings_json:
        if building[BID] == b_id:
            return True
    return False
