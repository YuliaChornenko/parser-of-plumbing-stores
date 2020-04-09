from flask import render_template, Response, request, redirect, url_for
from app import app
from app.db.get_db import read
from update_function.sandi_update import SandiUpdate
from update_function.antey_update import AnteyUpdate
from update_function.agromat_update import AgromatUpdate
from app.db.get_db import db, prepare_csv
import re

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view_db_select', methods=['GET', 'POST'])
def view_db_select():
    return render_template('view_db_select.html')

@app.route('/sandi_db', methods=['GET', 'POST'])
def sandi_db():
    file='sandi.csv'
    df = read(file)
    list_final = list()
    for lis in df:
        list_temp = list()
        for cat in lis:
            list_temp.append(cat+' : '+lis[cat][0])
        list_final.append(list_temp)
    return render_template('db_view.html', posts_even=list_final[::2], posts_odd = list_final[1::2])

@app.route('/antey_db', methods=['GET', 'POST'])
def antey_db():
    file='antey.csv'
    df = read(file)
    list_final = list()
    for lis in df:
        for cat in lis:
            list_final.append(cat+' : '+lis[cat][0])
    return render_template('db_view.html', posts=list_final)

@app.route('/agromat_db', methods=['GET', 'POST'])
def agromat_db():
    file='agromat.csv'
    df = read(file)
    list_final = list()
    for lis in df:
        for cat in lis:
            list_final.append(cat+' : '+lis[cat][0])
    return render_template('db_view.html', posts=list_final)

@app.route('/update_db', methods=['GET', 'POST'])
def update_db():
    site = request.form.get('site')
    print(site)
    if site:
        return redirect(url_for('update_db_select', site=site))
    return render_template('update_db.html', site=site)


@app.route('/update_db_select', methods=['GET', 'POST'])
def update_db_select():
    site = request.args.get('site')
    return render_template('update_db_select.html', site=site)

@app.route('/update_db_all', methods=['GET', 'POST'])
def update_db_all():
    site = request.args.get('site')
    print(site)
    print(site.split('/'))
    if site.split('/')[2] == 'b2b-sandi.com.ua':
        SandiUpdate.sandi_update_all(db, site)
        prepare_csv('sandi_db')
    elif site.split('/')[2] == 'b2b.antey.com.ua':
        AnteyUpdate.antey_update_all(db, site)
        prepare_csv('antey_db')
    elif site.split('/')[2] == 'partners.agromat.ua':
        AgromatUpdate.agromat_update_all(db, site)
        prepare_csv('agromat_db')
    else:
        return 'Проверьте корректность ссылки!'
    return 'База данных обновлена!'

@app.route('/update_db_price', methods=['GET', 'POST'])
def update_db_price():
    return 'price'

@app.route('/update_db_category', methods=['GET', 'POST'])
def update_db_category():
    return 'category'