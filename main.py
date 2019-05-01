from flask import Flask, jsonify, request
from users.login import login
from users.register import register
from buildings.apartments import get_apartments
from buildings.buildings import get_buildings, add_building, search
from buildings.common import get_apartments_and_buildings
from posts.posts import get_posts, add_post
from issues.issues import get_issues, add_issue
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="KHmZFwh4mA",
    passwd="hWP8GbQHs0",
    database="KHmZFwh4mA"
)

mycursor = mydb.cursor()

app.add_url_rule('/beta/login', methods=['POST'], view_func=login, defaults={'cursor': mycursor})

app.add_url_rule('/beta/register', methods=['POST'], view_func=register, defaults={'db': mydb})

app.add_url_rule('/beta/apartments/<u_id>', methods=['GET'], view_func=get_apartments, defaults={'cursor': mycursor})
app.add_url_rule('/beta/buildings/<u_id>', methods=['GET'], view_func=get_buildings, defaults={'cursor': mycursor})
app.add_url_rule('/beta/apartments_and_buildings/<u_id>', methods=['GET'],
                 view_func=get_apartments_and_buildings, defaults={'cursor': mycursor})

app.add_url_rule('/beta/add_building', methods=['POST'], view_func=add_building, defaults={'db': mydb})

app.add_url_rule('/beta/posts/<b_id>', methods=['GET'], view_func=get_posts, defaults={'cursor': mycursor})
app.add_url_rule('/beta/add_post', methods=['POST'], view_func=add_post, defaults={'db': mydb})

app.add_url_rule('/beta/issues/<b_id>', methods=['GET'], view_func=get_issues, defaults={'cursor': mycursor})
app.add_url_rule('/beta/add_issue', methods=['POST'], view_func=add_issue, defaults={'db': mydb})

app.add_url_rule('/beta/search/<content>', methods=['GET'], view_func=search, defaults={'cursor': mycursor})

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
