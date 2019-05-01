from constants.constants import *
from flask import jsonify, request
import time,datetime


def login(cursor):
    params = request.get_json()
    if MAIL in params and PASSWORD in params:
        cursor.execute('SELECT u_id FROM users where email=%s and pass=%s', (params[MAIL], params[PASSWORD]))
        myresult = cursor.fetchall()
        if len(myresult) > 0:
            current_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('UPDATE users SET last_login = %s WHERE email=%s and pass=%s',
                             (current_ts, params[MAIL], params[PASSWORD]))
            return jsonify({DATA: {UID: myresult[0][0]}})
        else:
            return jsonify({ERROR: "wrong email or password"})
    return jsonify({ERROR: "wrong details"})
