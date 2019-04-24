from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="KHmZFwh4mA",
    passwd="hWP8GbQHs0",
    database="KHmZFwh4mA"
)

mycursor = mydb.cursor()


@app.route('/beta/login/<mail>/<password>', methods=['GET'])
def login(mail, password):
    mycursor.execute('SELECT u_id FROM users where email=%s and pass=%s', (mail, password))
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return jsonify({'user_id': myresult[0][0]})
    return jsonify({})


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


@app.route('/beta/register/<name>/<email>/<password>/<phone_number>/', methods=['GET'])
def register(name, email, password, phone_number):
    try:
        mycursor.execute('INSERT INTO users (name,pass,email,phone_number) VALUES (%s,%s,%s,%s)',
                         (name, password, email, phone_number))
        mydb.commit()
        return jsonify({'data': str(mycursor.rowcount) + ' record inserted.'})
    except mysql.connector.errors.IntegrityError as e:
        return jsonify({'error': e.msg})


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
