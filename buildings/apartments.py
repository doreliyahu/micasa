from constants.constants import *
from flask import jsonify


def get_apartments(cursor, u_id):
    result = []
    cursor.execute('select a.b_id, a.a_id, a.floor, a.a_number, b.country,b.city,b.street,b.number,b.name' +
                   ' from apartments as a left outer join residence as r on r.a_id = a.a_id' +
                   ' LEFT OUTER JOIN buildings as b on a.b_id = b.b_id where r.u_id = "' + u_id + '"')
    apartments = cursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            AID: apartment[1],
            FLOOR: apartment[2],
            ANUMBER: apartment[3],
            COUNTRY: apartment[4],
            CITY: apartment[5],
            STREET: apartment[6],
            NUMBER: apartment[7],
            NAME: apartment[8],
        })
    return jsonify({DATA: result})


def get_apartments_array(apartments_json, b_id):
    result = []
    for apartment in apartments_json:
        if apartment[BID] == b_id:
            result.append(apartment)
    return result
