from flask import render_template, Response, request, redirect, url_for
from app import app
from app.db.get_db import read


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view_db_select', methods=['GET', 'POST'])
def view_db_select():
    return render_template('view_db_select.html')

@app.route('/sandi_db', methods=['GET', 'POST'])
def sandi_db():
    df = read()
    return render_template('db_view.html', posts=df)


@app.route('/update_db', methods=['GET', 'POST'])
def update_db():
    site = request.form.get('site')
    print(site)
    if site:
        return redirect(url_for('update_db_select', site=site))
    return render_template('update_db.html', site=site)


@app.route('/update_db_select', methods=['GET', 'POST'])
def update_db_select():
    return render_template('update_db_select.html')

@app.route('/update_db_all', methods=['GET', 'POST'])
def update_db_all():
    return 'all'

@app.route('/update_db_price', methods=['GET', 'POST'])
def update_db_price():
    return 'price'

@app.route('/update_db_category', methods=['GET', 'POST'])
def update_db_category():
    return 'category'