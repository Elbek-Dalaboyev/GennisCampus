from flask import Flask, jsonify, abort, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Auth, Locations

import sys
import bcrypt
import hashlib


def create_app(test_config=True):
    app = Flask(__name__)
    setup_db(app)

    @app.route('/')
    def home():
        return render_template('html/index.html')

    @app.route('/auth_list/<int:list_id>')
    def list_func(list_id):

        return render_template('html/auth_list.html',
            lists=Locations.query.all(),
            id_list=Auth.query.filter(Auth.locations == list_id).all()
        )

    @app.route('/auth_list')
    def index():
        return redirect(url_for('list_func', list_id=1))

    @app.route('/sign')
    def sign():
        return render_template('html/login.html')

    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        email = request.form.get('email_sign_in')
        phone = request.form.get('number_sign_in')
        password = request.form.get('password_sign_in')
        pass_w = hashlib.md5(password.encode()).hexdigest()

        if email and password and not phone:
            pass
        elif phone and password and not email:
            pass
        else:
            abort(422)





        return render_template('html/home.html')

    @app.route('/sign_up', methods=['POST'])
    def sign_up():

        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        second_phone = request.form.get('second_phone')
        location = request.form.get('location')

        if name == '':
            abort(422)
        if surname == '':
            abort(422)
        if email == '':
            abort(422)
        if password == '':
            abort(422)

        if location == "hojakent":
            location = 1
        elif location == "gazalkent":
            location = 2
        hashed = hashlib.md5(password.encode()).hexdigest()

        log_ins = Auth(
            name=name,
            surname=surname,
            email=email,
            password=hashed,
            phone=phone,
            second_phone=second_phone,
            locations=location,
            image_link=None,
            permission=None
        )

        log_ins.insert()

        return redirect(url_for('home'))

    @app.route('/search/', methods=['POST'])
    def search_name():
        answer = ''
        result = request.form.get('search')
        if Auth.query.filter(Auth.id.ilike(result)):
            answer = Auth.query.filter(Auth.id.ilike(f'{result}'))
        if Auth.query.filter(Auth.name.ilike(f'{result}')):
            answer = Auth.query.filter(Auth.name.ilike(f'{result}'))
        elif Auth.query.filter(Auth.surname.ilike(f'{result}')):
            answer = Auth.query.filter(Auth.surname.ilike(f'{result}'))
        else:
            abort(404)

        return render_template('html/auth_list.html', res=answer)



    return app


app = create_app()