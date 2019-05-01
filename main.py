from flask import Flask, jsonify, request
import mysql.connector
import uuid,datetime,time


app = Flask(__name__)

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="KHmZFwh4mA",
    passwd="hWP8GbQHs0",
    database="KHmZFwh4mA"
)

mycursor = mydb.cursor()


MAIL = 'email'
PASSWORD = 'password'
NAME = 'name'
PHONE_NUMBER = 'phone_number'
BID = 'b_id'
UID = 'u_id'
AID = 'a_id'
IID = 'i_id'
PID = 'p_id'
CONTENT = 'content'
STATUS = 'status'
CATEGORY = 'category'
DT = 'dt'
IMAGE1 = 'image1'
IMAGE2 = 'image2'
IMAGE3 = 'image3'
COUNTRY = 'country'
CITY = 'city'
STREET = 'street'
AVATAR = 'avatar'
NUMBER = 'number'
CREATION_TIME = 'creation_time'
DATA = 'data'
ERROR = 'error'


@app.route('/beta/login', methods=['POST'])
def login():
    params = request.get_json()
    if MAIL in params and PASSWORD in params:


        mycursor.execute('SELECT u_id FROM users where email=%s and pass=%s', (params[MAIL], params[PASSWORD]))
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            current_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            mycursor.execute('UPDATE users SET last_login = %s WHERE email=%s and pass=%s',
                             (current_ts, params[MAIL], params[PASSWORD]))
            mydb.commit()
            return jsonify({DATA: {UID: myresult[0][0]}})
        else:
            return jsonify({ERROR: "wrong email or password"})
    return jsonify({ERROR: "wrong details"})


@app.route('/beta/register', methods=['POST'])
def register():
    try:
        params = request.get_json()
        if PHONE_NUMBER not in params:
            params[PHONE_NUMBER] = None
        if MAIL in params and NAME in params and PASSWORD in params:
            guid = str(uuid.uuid4())
            mycursor.execute('INSERT INTO users (u_id,name,pass,email,phone_number) VALUES (%s,%s,%s,%s,%s)',
                             (guid, params[NAME], params[PASSWORD], params[MAIL], params[PHONE_NUMBER]))
            mydb.commit()
            return jsonify({DATA: {UID: guid}})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


@app.route('/beta/apartments/<u_id>', methods=['GET'])
def get_apartments(u_id):
    result = []
    mycursor.execute('select a.b_id, a.a_id, b.country,b.city,b.street,b.number' +
                     ' from apartments as a left outer join residence as r on r.a_id = a.a_id' +
                     ' LEFT OUTER JOIN buildings as b on a.b_id = b.b_id where r.u_id = ' + u_id)
    apartments = mycursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            AID: apartment[1],
            COUNTRY: apartment[2],
            CITY: apartment[3],
            STREET: apartment[4],
            NUMBER: apartment[5],
        })
    return jsonify({DATA: result})


@app.route('/beta/buildings/<u_id>', methods=['GET'])
def get_buildings(u_id):
    result = []
    mycursor.execute('select m.b_id, m.is_admin,b.country,b.city,b.street,b.number from management as m ' +
                     'LEFT OUTER JOIN buildings as b on m.b_id = b.b_id where m.u_id =' + u_id)
    apartments = mycursor.fetchall()
    for apartment in apartments:
        result.append({
            BID: apartment[0],
            'is_admin': apartment[1],
            COUNTRY: apartment[2],
            CITY: apartment[3],
            STREET: apartment[4],
            NUMBER: apartment[5],
        })
    return jsonify({DATA: result})


@app.route('/beta/apartments_and_buildings/<u_id>', methods=['GET'])
def get_apartments_and_buildings(u_id):
    j1 = get_apartments(u_id)
    j2 = get_buildings(u_id)
    return jsonify({DATA: (j1.json[DATA] + j2.json[DATA])})


@app.route('/beta/add_building', methods=['POST'])
def add_building():
    try:
        params = request.get_json()
        if NAME not in params:
            params[NAME] = None
        if COUNTRY in params and CITY in params and STREET in params and NUMBER in params:
            guid = str(uuid.uuid4())
            mycursor.execute('INSERT INTO buildings (b_id,country,city,street,number,name) VALUES (%s,%s,%s,%s,%s,%s)',
                             (guid,params[COUNTRY], params[CITY], params[STREET], params[NUMBER], params[NAME]))
            mydb.commit()
            return jsonify({DATA: {"b_id": guid}})
        return jsonify({ERROR: "wrong parameters"})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


@app.route('/beta/posts/<b_id>', methods=['GET'])
def get_posts(b_id):
    result = []
    mycursor.execute('select * from posts as p left OUTER join users as u on p.u_id = u.u_id where b_id=' + b_id)
    apartments = mycursor.fetchall()
    for apartment in apartments:
        result.append({
            PID: apartment[0],
            BID: apartment[1],
            'user': {
                NAME: apartment[10],
                UID: apartment[2],
                AVATAR: apartment[13]
            },
            CONTENT: apartment[3],
            DT: apartment[4],
            IMAGE1: apartment[5],
            IMAGE2: apartment[6],
            IMAGE3: apartment[7],
        })
    return jsonify({DATA: result})


@app.route('/beta/add_post', methods=['POST'])
def add_post():
    try:
        params = request.get_json()
        if IMAGE1 not in params:
            params[IMAGE1]=None
        if IMAGE2 not in params:
            params[IMAGE2]=None
        if IMAGE3 not in params:
            params[IMAGE3]=None
        if BID in params and CONTENT in params and DT in params and UID in params:
            guid = str(uuid.uuid4())
            mycursor.execute('INSERT INTO posts (p_id,b_id,u_id,content,dt,image1,image2,image3) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                             (guid, params[UID], params[CONTENT], params[DT], params[IMAGE1], params[IMAGE2], params[IMAGE3]))
            mydb.commit()
            return jsonify({DATA: {PID: guid}})
        return jsonify({ERROR: "wrong parameters"})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


@app.route('/beta/add_issue', methods=['POST'])
def add_post():
    try:
        params = request.get_json()
        if CONTENT in params and IID in params and CATEGORY in params and UID in params and BID in params:
            guid = str(uuid.uuid4())
            mycursor.execute('INSERT INTO issues (i_id,b_id,u_id,content,category,creation_time,status) VALUES (%s,%s,%s,%s,%s,%s,%d)',
                             (guid, params[BID], params[UID], params[CONTENT], params[CATEGORY], params[CREATION_TIME], 0))
            mydb.commit()
            return jsonify({DATA: {IID: guid}})
        return jsonify({ERROR: "wrong parameters"})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({ERROR: e.msg})


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
