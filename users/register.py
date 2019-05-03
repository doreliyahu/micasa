from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def register(db):
    try:
        params = request.get_json()
        if PHONE_NUMBER not in params:
            params[PHONE_NUMBER] = None
        if MAIL in params and NAME in params and PASSWORD in params:
            guid = str(uuid.uuid4())
            result = db.connect().execute(
                'INSERT INTO users (u_id,name,pass,email,phone_number) VALUES (%s,%s,%s,%s,%s)',
                (guid, params[NAME], params[PASSWORD], params[MAIL], params[PHONE_NUMBER]))
            if result.rowcount > 0:
                return jsonify({DATA: {UID: guid}})
            else:
                return jsonify({ERROR: ZERO_ROWS_AFFECTED})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})
