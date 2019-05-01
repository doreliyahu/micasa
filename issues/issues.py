from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def get_issues(cursor, b_id):
    pass


def add_issue(db):
    try:
        params = request.get_json()
        if CONTENT in params and CATEGORY in params and UID in params and BID in params:
            guid = str(uuid.uuid4())
            db.cursor().execute(
                'INSERT INTO issues (i_id,b_id,u_id,content,category,creation_time,status) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                (guid, params[BID], params[UID], params[CONTENT], params[CATEGORY], params[CREATION_TIME], "0"))
            db.commit()
            return jsonify({DATA: {IID: guid}})
        return jsonify({ERROR: "wrong parameters"})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})
