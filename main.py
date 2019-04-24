from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/tests/test1', methods=['GET'])
def get_tasks():
    return jsonify({'test1_results': tasks})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
