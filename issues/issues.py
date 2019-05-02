from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def get_issues(cursor, b_id):
    result = []
    query = 'select * from issues as i left OUTER join users as u on i.u_id = u.u_id where b_id="' + b_id + '"'
    cursor.execute(query)
    issues = cursor.fetchall()
    for issue in issues:
        result.append({
            IID: issue[0],
            BID: issue[1],
            'user': {
                NAME: issue[9],
                UID: issue[2],
                AVATAR: issue[13]
            },
            CATEGORY: issue[3],
            CONTENT: issue[4],
            STATUS: issue[5],
            CREATION_TIME: issue[6]
        })
    return jsonify({DATA: result})


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
