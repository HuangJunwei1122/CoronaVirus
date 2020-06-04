from flask import flash, url_for, render_template, redirect, jsonify, request, session
# from flask_wtf.csrf import validate_csrf
# from wtforms import ValidationError
import datetime

from CoronaVirus import app
from CoronaVirus.forms import DateForm
from CoronaVirus.get_daily_confirmed import output_one_csv
from CoronaVirus.utils import TODAY, ONE_DAY, LAST_DAY, START_DAY, get_confirmed, verify_date, fetch_daily


@app.route('/<date>', methods=['GET', 'POST'])
@app.route('/', defaults={'date': LAST_DAY.strftime('%Y-%m-%d')}, methods=['GET', 'POST'])
def index(date):
    form = DateForm()
    # flash('输入日期范围：2020-1-22至{}'.format(LAST_DAY))
    if request.method == 'POST':
        # try:
        #     validate_csrf(form.csrf_token.data)
        # except ValidationError:
        #     flash('CSRF token error.')
        #     return redirect(url_for('index'))
        date = form.date.data
        if not date:
            flash('请输入正确格式的日期')
            return redirect(url_for('index'))
        elif verify_date(date):
            # print('正确')
            return redirect(url_for('index', date=date.strftime('%Y-%m-%d')))
        flash('请输入2020-1-22至{}的日期'.format(LAST_DAY))
        return redirect(url_for('index'))
    return render_template('index.html', form=form, date=date)


@app.route('/search', methods=['POST'])
def search():
    form = DateForm()
    if request.method == 'POST':
        # try:
        #     validate_csrf(form.csrf_token.data)
        # except ValidationError:
        #     flash('CSRF token error.')
        #     return redirect(url_for('index'))
        date = form.date.data
        if not date:
            flash('请输入正确格式的日期')
        elif verify_date(date):
            # print('正确')
            return redirect(url_for('index', date=date.strftime('%Y-%m-%d')))
        else:
            flash('请输入2020-1-22至{}的日期'.format(LAST_DAY))
    return redirect(url_for('index'))


@app.route('/data')
def data():
    date = request.args.get('date', LAST_DAY)
    pre = request.args.get('pre', False)
    after = request.args.get('after', False)
    if not isinstance(date, datetime.date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    if pre and date > START_DAY:
        date -= ONE_DAY
    if after and date < (TODAY - ONE_DAY):
        date += ONE_DAY
    # confirmed, active = get_confirmed(date)
    data_set = get_confirmed(date)
    # return jsonify(confirmed=confirmed, active=active, date=date.strftime('%Y-%m-%d'))
    return jsonify(data_set=data_set, date=date.strftime('%Y-%m-%d'))


@app.route('/test')
def test():
    # output_one_csv()
    # fetch_daily()
    return redirect(url_for('index'))
