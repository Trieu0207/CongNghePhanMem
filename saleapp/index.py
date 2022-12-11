import cloudinary.uploader
from flask import render_template, request, redirect, url_for
from saleapp import app, controller
import dao
from cloudinary import uploader
import re
from saleapp.admin import *
@app.route('/', methods=['get','post'])
def home():
    global tuyen_bay
    tuyen = dao.load_tuyen_bay_by_kw(kw=request.args.get('keyword'))
    all_tuyen = dao.load_tuyen_bay()
    ten_diem_di = dao.load_ten_diem_di()
    ten_diem_den = dao.load_ten_diem_den()
    if request.method.__eq__('POST'):
        diem_di = request.form['diem_di']
        diem_den = request.form['diem_den']
        tuyen_bay = dao.search_tuyen_bay(diem_di, diem_den)
        return render_template('index.html',tuyen_bay = tuyen_bay,
                               ten_diem_den = ten_diem_den,
                               ten_diem_di = ten_diem_di)
    return render_template('index.html', tuyen = tuyen, all_tuyen = all_tuyen,
                           ten_diem_den = ten_diem_den, ten_diem_di = ten_diem_di)

@app.route('/chuyen_bay/<int:tuyen_bay_id>')
def chuyen_bay(tuyen_bay_id):
    chuyen = dao.load_chuyen_bay_by_tuyen_bay_id(tuyen_bay_id)
    ten_diem_den = dao.load_ten_diem_den()
    ten_diem_di = dao.load_ten_diem_di()
    if chuyen:
        tuyen = dao.load_tuyen_bay_by_id(tuyen_bay_id)
        san_di = dao.search_san_bay_by_id(chuyen[0].san_bay_di_id).ten_san_bay
        san_den = dao.search_san_bay_by_id(chuyen[0].san_bay_den_id).ten_san_bay
        lich_bay = dao.load_lich_bay(chuyen)
        gia_ve_normal = dao.load_gia_ve_by_chuyen_bay(tuyen_bay_id, "normal")
        gia_ve_vip = dao.load_gia_ve_by_chuyen_bay(tuyen_bay_id, "vip")
        return render_template('chuyenBays.html', ten_diem_den = ten_diem_den,
                               ten_diem_di = ten_diem_di, chuyen=chuyen, tuyen=tuyen,
                               san_di = san_di, san_den = san_den, lich_bay = lich_bay,
                               gia_ve_normal = gia_ve_normal, gia_ve_vip = gia_ve_vip)
    return render_template('chuyenBays.html', chuyen = chuyen)
@app.route('/ve/<int:chuyen_bay_id>')
def ve(chuyen_bay_id):
    ds_ghe = dao.load_ds_ghe(chuyen_bay_id)
    table_ghe = dao.load_table_ghe(chuyen_bay_id)
    return render_template('ve.html', ds_ghe = ds_ghe, table_ghe = table_ghe)
@app.route('/register', methods=['get', 'post'])
def user_register():
    ex=""
    global ho_ten, ngay_thang_nam_sinh, email, sdt, ten_dang_nhap, mat_khau
    if request.method.__eq__('POST'):
        ho_ten = request.form['first_name']
        ngay_thang_nam_sinh = request.form['birth_day']
        email = request.form['email']
        sdt = request.form['sdt']
        ten_dang_nhap = request.form['user_name']
        mat_khau = request.form['pass']
    try:
        avatar = ''

        if request.files:
            res = cloudinary.uploader.upload(request.files['avatar'])
            avatar = res['secure_url']
        dao.register(ho_va_ten = ho_ten, ngay_sinh=ngay_thang_nam_sinh,
                     email = email, sdt = sdt, ten_dang_nhap = ten_dang_nhap, mat_khau = mat_khau, avatar = avatar)
        return redirect('/')
    except Exception as e:
        ex = str(e)

    return render_template('register.html', method =['get', 'post'], ex = ex)
@app.route('/login', methods=['get', 'post'])
def user_login():
    ex=""
    if request.method.__eq__('POST'):
        user_name = request.form['user_name']
        password = request.form['password']
        try:
            dao.login(user_name = user_name, password = password)
            return redirect('/')
        except Exception as e:
            ex = str(e)
    return render_template('login.html', ex = ex)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)