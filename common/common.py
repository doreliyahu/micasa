from flask import jsonify
from constants.constants import *
from users.login import login
from buildings.common import get_apartments_and_buildings


def fetch_login(db):
    login_res = login(db).json
    if DATA in login_res:
        result = {}
        a_and_b = get_apartments_and_buildings(db, login_res[DATA][UID]).json[DATA]
        user = login_res[DATA]
        return jsonify({
            DATA: {
                BUILDINGS: a_and_b,
                USER: user
            }
        })
    else:
        return jsonify(login_res)
