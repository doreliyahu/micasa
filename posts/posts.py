from constants.constants import *
from flask import jsonify, request
import uuid
import mysql.connector


def get_posts(db, b_id):
    result = []
    query = 'select * from posts as p left OUTER join users as u on p.u_id = u.u_id where b_id="' + b_id + '"'
    posts = db.connect().execute(query).cursor.fetchall()
    for post in posts:
        result.append({
            PID: post[0],
            BID: post[1],
            USER: {
                NAME: post[10],
                UID: post[2],
                AVATAR: post[13]
            },
            CONTENT: post[3],
            DT: post[4],
            IMAGE1: post[5],
            IMAGE2: post[6],
            IMAGE3: post[7],
        })
    return jsonify({DATA: result})


def add_post(db):
    try:
        params = request.get_json()
        if IMAGE1 not in params:
            params[IMAGE1] = None
        if IMAGE2 not in params:
            params[IMAGE2] = None
        if IMAGE3 not in params:
            params[IMAGE3] = None
        if BID in params and CONTENT in params and DT in params and UID in params:
            guid = str(uuid.uuid4())
            result = db.connect().execute(
                'INSERT INTO posts (p_id,b_id,u_id,content,dt,image1,image2,image3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                (guid, params[BID], params[UID], params[CONTENT], params[DT], params[IMAGE1], params[IMAGE2],
                 params[IMAGE3]))
            if result.rowcount > 0:
                return jsonify({DATA: {PID: guid}})
            else:
                return jsonify({ERROR: ZERO_ROWS_AFFECTED})
        return jsonify({ERROR: WRONG_PARAMETERS})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})
