import time
import threading
from flask import Flask, jsonify, request
from users.login import login
from users.register import register
from buildings.apartments import get_apartments
from buildings.buildings import get_buildings, add_building, search
from buildings.common import get_apartments_and_buildings
from posts.posts import get_posts, add_post
from issues.issues import get_issues, add_issue
from common.common import fetch_login
from sqlalchemy import create_engine

app = Flask(__name__)


def main():
    db = create_engine("mysql+pymysql://KHmZFwh4mA:hWP8GbQHs0@remotemysql.com/KHmZFwh4mA")

    app.add_url_rule('/beta/fetch_login', methods=['POST'], view_func=fetch_login, defaults={'db': db})

    app.add_url_rule('/beta/login', methods=['POST'], view_func=login, defaults={'db': db})

    app.add_url_rule('/beta/register', methods=['POST'], view_func=register, defaults={'db': db})

    app.add_url_rule('/beta/apartments/<u_id>', methods=['GET'], view_func=get_apartments,
                     defaults={'db': db})
    app.add_url_rule('/beta/buildings/<u_id>', methods=['GET'], view_func=get_buildings, defaults={'db': db})
    app.add_url_rule('/beta/apartments_and_buildings/<u_id>', methods=['GET'],
                     view_func=get_apartments_and_buildings, defaults={'db': db})

    app.add_url_rule('/beta/add_building', methods=['POST'], view_func=add_building, defaults={'db': db})

    app.add_url_rule('/beta/posts/<b_id>', methods=['GET'], view_func=get_posts, defaults={'db': db})
    app.add_url_rule('/beta/add_post', methods=['POST'], view_func=add_post, defaults={'db': db})

    app.add_url_rule('/beta/issues/<b_id>', methods=['GET'], view_func=get_issues, defaults={'db': db})
    app.add_url_rule('/beta/add_issue', methods=['POST'], view_func=add_issue, defaults={'db': db})

    app.add_url_rule('/beta/search/<content>', methods=['GET'], view_func=search, defaults={'db': db})
    app.add_url_rule('/beta/search/<content>', methods=['GET'], view_func=search, defaults={'db': db})

    time.sleep(3600)


def run_app():
    app.run(port=80, host='0.0.0.0', debug=False)


if __name__ == '__main__':
    threading.Thread(target=run_app).start()
    while True:
        main()
