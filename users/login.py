from constants.constants import *
from flask import jsonify, request
import time, datetime


def login(db):
    params = request.get_json()
    if MAIL in params and PASSWORD in params:
        myresult = db.connect().execute(
            'SELECT u_id,email,name,phone_number,avatar FROM users where email=%s and pass=%s',
            (params[MAIL], params[PASSWORD])).cursor.fetchall()
        if len(myresult) > 0:
            current_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            db.connect().execute('UPDATE users SET last_login = %s WHERE email=%s and pass=%s',
                                 (current_ts, params[MAIL], params[PASSWORD]))
            myresult = myresult[0]
            return jsonify({DATA: {
                UID: myresult[0],
                MAIL: myresult[1],
                NAME: myresult[2],
                PHONE_NUMBER: myresult[3],
                AVATAR: myresult[4]
            }})
        else:
            return jsonify({ERROR: "wrong email or password"})
    return jsonify({ERROR: "wrong details"})
