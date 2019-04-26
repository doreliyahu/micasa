from flask import Flask, jsonify, request
import mysql.connector
import ast
app = Flask(__name__)

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="KHmZFwh4mA",
    passwd="hWP8GbQHs0",
    database="KHmZFwh4mA"
)

mycursor = mydb.cursor()


MAIL = 'mail'
PASSWORD = 'password'
NAME = 'name'
PHONE_NUMBER = 'phone_number'


@app.route('/beta/login', methods=['POST'])
def login():
    params = ast.literal_eval(request.get_json())
    if (MAIL in params or PHONE_NUMBER in params) and PASSWORD in params:
        if MAIL in params:
            mycursor.execute('SELECT u_id FROM users where email=%s and pass=%s', (params[MAIL], params[PASSWORD]))
        elif PHONE_NUMBER in params:
            mycursor.execute('SELECT u_id FROM users where phone_number=%s and pass=%s', (params[PHONE_NUMBER], params[PASSWORD]))
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            return jsonify({'user_id': myresult[0][0]})
    return jsonify({'error': 'wrong details'})


@app.route('/beta/register/', methods=['POST'])
def register():
    try:
        params = ast.literal_eval(request.get_json())
        if (MAIL in params or PHONE_NUMBER in params) and NAME in params and PASSWORD in params:
            mycursor.execute('INSERT INTO users (name,pass,email,phone_number) VALUES (%s,%s,%s,%s)',
                             (params[NAME], params[PASSWORD], params[MAIL], params[PHONE_NUMBER]))
            mydb.commit()
            return jsonify({'data': str(mycursor.rowcount) + ' record inserted.'})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({'error': e.msg})


@app.route('/beta/apartments/<u_id>', methods=['GET'])
def get_apartments(u_id):
    result = []
    mycursor.execute('select a.b_id, a.a_id, b.country,b.city,b.street,b.number' +
                     ' from apartments as a left outer join residence as r on r.a_id = a.a_id' +
                     ' LEFT OUTER JOIN buildings as b on a.b_id = b.b_id where r.u_id = ' + u_id)
    apartments = mycursor.fetchall()
    for apartment in apartments:
        result.append({
            'b_id': apartment[0],
            'a_id': apartment[1],
            'country': apartment[2],
            'city': apartment[3],
            'street': apartment[4],
            'number': apartment[5],
        })
    return jsonify({'data': result})


@app.route('/beta/buildings/<u_id>', methods=['GET'])
def get_buildings(u_id):
    result = []
    mycursor.execute('select m.b_id, m.is_admin,b.country,b.city,b.street,b.number from management as m ' +
                     'LEFT OUTER JOIN buildings as b on m.b_id = b.b_id where m.u_id =' + u_id)
    apartments = mycursor.fetchall()
    for apartment in apartments:
        result.append({
            'b_id': apartment[0],
            'is_admin': apartment[1],
            'country': apartment[2],
            'city': apartment[3],
            'street': apartment[4],
            'number': apartment[5],
        })
    return jsonify({'data': result})


@app.route('/beta/apartments_and_buildings/<u_id>', methods=['GET'])
def get_apartments_and_buildings(u_id):
    j1 = get_apartments(u_id)
    j2 = get_buildings(u_id)
    return jsonify({'data': (j1.json['data'] + j2.json['data'])})


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
