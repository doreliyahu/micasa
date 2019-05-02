from constants.constants import *
from flask import jsonify
from . import buildings as b
from . import apartments as a


def get_apartments_and_buildings(cursor, u_id):
    apartments = a.get_apartments(cursor, u_id).json[DATA]
    buildings = b.get_buildings(cursor, u_id).json[DATA]
    result = []
    for apartment in apartments:
        if not b.is_building_exists(buildings,apartment[BID]):
            result.append({
                BID: apartment[BID],
                PERMISSION: 0,
                COUNTRY: apartment[COUNTRY],
                CITY: apartment[CITY],
                STREET: apartment[STREET],
                NUMBER: apartment[NUMBER],
                NAME: apartment[NAME],
                APARTMENTS: a.get_apartments_array(apartments, apartment[BID])
            })
    for building in buildings:
        result.append({
            BID: building[BID],
            PERMISSION: 1 + building[IS_ADMIN],
            COUNTRY: building[COUNTRY],
            CITY: building[CITY],
            STREET: building[STREET],
            NUMBER: building[NUMBER],
            NAME: building[NAME],
            APARTMENTS: a.get_apartments_array(apartments, building[BID])
        })
    return jsonify({DATA: result})
