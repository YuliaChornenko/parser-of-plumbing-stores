from flask import render_template, Response, request, redirect, url_for, send_from_directory, send_file
from app import app
from app.db.get_db import db
from scraper.scraper_1 import Scraper
from scraper.scraper_2 import get_agromat_brands
from tasks import sandi_update_all, sandi_update_prices, sandi_brands_update, antey_update_all, antey_update_prices, antey_brands_update, agromat_update_all, agromat_update_prices, agromat_brands_update, prepare_csv

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view_db_select', methods=['GET', 'POST'])
def view_db_select():
    return render_template('view_db_select.html')

@app.route('/sandi_db', methods=['GET', 'POST'])
def sandi_db():
    prepare_csv('sandi_db')
    path = "db/data/sandi_db.xlsx"
    return send_file(path, as_attachment=True)

@app.route('/antey_db', methods=['GET', 'POST'])
def antey_db():
    path = "db/data/antey_db.xlsx"
    return send_file(path, as_attachment=True)

@app.route('/agromat_db', methods=['GET', 'POST'])
def agromat_db():
    path = "db/data/agromat_db.xlsx"
    return send_file(path, as_attachment=True)

@app.route('/update_db', methods=['GET', 'POST'])
def update_db():
    site = request.form.get('site')
    print(site)
    if site:
        return redirect(url_for('update_db_select', site=site))
    return render_template('update_db.html', site=site)

@app.route('/update_db_select', methods=['GET', 'POST'])
def update_db_select():
    site = request.args.get('site').strip()
    return render_template('update_db_select.html', site=site)

@app.route('/update_db_all', methods=['GET', 'POST'])
def update_db_all():
    site = request.args.get('site').strip()
    if site.split('/')[2] == 'b2b-sandi.com.ua':
        sandi_update_all(db,site)
    elif site.split('/')[2] == 'b2b.antey.com.ua':
        antey_update_all(db, site)
        prepare_csv('antey_db')
    elif site.split('/')[2] == 'partners.agromat.ua':
        agromat_update_all(db, site)
        prepare_csv('agromat_db')
    else:
        return 'Проверьте корректность ссылки!'
    return 'База данных обновлена!'

@app.route('/update_db_price', methods=['GET', 'POST'])
def update_db_price():
    site = request.args.get('site').strip()
    if site.split('/')[2] == 'b2b-sandi.com.ua':
        sandi_update_prices(db, site)
        prepare_csv('sandi_db')
    elif site.split('/')[2] == 'b2b.antey.com.ua':
        antey_update_prices(db, site)
        prepare_csv('antey_db')
    elif site.split('/')[2] == 'partners.agromat.ua':
        agromat_update_prices(db, site)
        prepare_csv('agromat_db')
    else:
        return 'Проверьте корректность ссылки!'
    return 'База данных обновлена!'

@app.route('/update_db_brand_select', methods=['GET', 'POST'])
def update_db_brand_select():
    site = request.args.get('site').strip()
    if site.split('/')[2] == 'b2b-sandi.com.ua':
        posts = Scraper.get_sandi_brands(Scraper.get_soup(site))
    elif site.split('/')[2] == 'b2b.antey.com.ua':
        posts = Scraper.get_antey_brands(Scraper.get_soup(site))
    elif site.split('/')[2] == 'partners.agromat.ua':
        posts = get_agromat_brands(site)
    else:
        return 'Проверьте корректность ссылки!'
    return render_template('update_db_brand_select.html', posts=posts, site=site)

@app.route('/update_db_brand', methods=['GET', 'POST'])
def update_db_brand():
    site = request.args.get('site')
    cat = request.form.getlist('cat')
    if site.split('/')[2] == 'b2b-sandi.com.ua':
        sandi_brands_update(db, site, cat)
        prepare_csv('sandi_db')
    elif site.split('/')[2] == 'b2b.antey.com.ua':
        antey_brands_update(db, site, cat)
        prepare_csv('antey_db')
    elif site.split('/')[2] == 'partners.agromat.ua':
        agromat_brands_update(db, site, cat)
        prepare_csv('agromat_db')
    else:
        return 'Проверьте корректность ссылки!'
    return 'База данных обновлена!'

