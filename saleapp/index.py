from flask import render_template, request
from saleapp import app, controller
import dao
from saleapp.admin import *
@app.route('/')
def home():
    tuyen = dao.load_tuyen_bay_by_kw(kw=request.args.get('keyword'))
    all_tuyen = dao.load_tuyen_bay()
    ten_diem_di = dao.load_ten_diem_di()
    ten_diem_den = dao.load_ten_diem_den()
    return render_template('index.html', tuyen = tuyen, all_tuyen = all_tuyen,
                           ten_diem_den = ten_diem_den, ten_diem_di = ten_diem_di)

@app.route('/chuyen_bay/<int:tuyen_bay_id>')
def chuyen_bay(tuyen_bay_id):
    chuyen = dao.load_chuyen_bay_by_tuyen_bay_id(tuyen_bay_id)
    ten_diem_den = dao.load_ten_diem_den()
    ten_diem_di = dao.load_ten_diem_di()
    return render_template('chuyenBays.html', ten_diem_den = ten_diem_den, ten_diem_di = ten_diem_di)

@app.route('/register')
def user_register():
    return render_template('register.html', method =['get', 'post'])


if __name__ == '__main__':
    app.run(debug=True)