from saleapp import app, db
from saleapp.models import Tuyen_bay, Chuyen_bay, Nguoi_dung, San_bay, Lich_bay, Ghe, Ve_may_bay
from sqlalchemy import or_, and_
import hashlib
import re
from datetime import datetime
from datetime import date


def load_tuyen_bay():
    return Tuyen_bay.query.all()


def load_tuyen_bay_by_kw(kw=None):
    query = Tuyen_bay.query.all()
    if kw:
        query = Tuyen_bay.query.filter(or_(Tuyen_bay.diem_di.__eq__(kw),
                                           Tuyen_bay.diem_den.__eq__(kw),
                                           Tuyen_bay.ten.__eq__(kw),
                                           Tuyen_bay.id.__eq__(kw))).all()
    return query


def load_ten_diem_di():
    temp = Tuyen_bay.query.all()
    diem_di = []
    for t in temp:
        if t.diem_di not in diem_di:
            diem_di.append(t.diem_di)
    return sorted(diem_di)


def load_ten_diem_den():
    temp = Tuyen_bay.query.all()
    diem_den = []
    for t in temp:
        if t.diem_den not in diem_den:
            diem_den.append(t.diem_den)
    diem_den = sorted(diem_den)
    return sorted(diem_den)


def login(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    try:
        check_login(user_name, password)
    except Exception as ex:
        raise Exception(ex)


def register(ho_va_ten, ngay_sinh, email, sdt, ten_dang_nhap, mat_khau, **kwargs):
    ds_nguoi_dung = []
    check_pass = mat_khau
    if not strong_pass(check_pass):
        raise Exception("mật khẩu không hợp lệ")
    if not check_sdt(sdt):
        raise Exception("số điện thoại không hợp lệ")
    if not check_birth_day(ngay_sinh):
        raise Exception('Ngày sinh không hợp lệ')
    password = str(hashlib.md5(mat_khau.strip().encode('utf-8')).hexdigest())
    for d in Nguoi_dung.query.all():
        if d.ten_dang_nhap == ten_dang_nhap:
            ds_nguoi_dung.append(d.ten_dang_nhap)
    if ten_dang_nhap not in ds_nguoi_dung:
        nguoi_dung = Nguoi_dung(ho_va_ten=ho_va_ten.strip(),
                                ngay_thang_nam_sinh=ngay_sinh,
                                email=email.strip(),
                                sdt=sdt.strip(),
                                ten_dang_nhap=ten_dang_nhap.strip(),
                                mat_khau=password,
                                avatar=kwargs.get('avatar'))
        with app.app_context():
            db.session.add(nguoi_dung)
            db.session.commit()
    else:
        raise Exception("tên đăng nhập đã tồn tại")


def search_tuyen_bay(diem_di, diem_den):
    query = Tuyen_bay.query.filter(and_(Tuyen_bay.diem_di.__eq__(diem_di),
                                        Tuyen_bay.diem_den.__eq__(diem_den))).first()
    return query


def load_tuyen_bay_by_id(tuyen_bay_id):
    return Tuyen_bay.query.get(tuyen_bay_id)


def load_chuyen_bay_by_tuyen_bay_id(tuyen_bay_id):
    return Chuyen_bay.query.filter(Chuyen_bay.tuyen_bay_id == tuyen_bay_id).all()


def strong_pass(client_pass):
    pass_lenght = len(client_pass) > 8
    pass_up = re.search(r"[A-Z]", client_pass) is not None
    pass_low = re.search(r"[a-z]", client_pass) is not None
    pass_ok = not (pass_lenght or pass_low or pass_up)
    if (pass_lenght and pass_low and pass_up):
        return True
    else:
        return False


def check_sdt(client_sdt):
    sdt_lenght = len(client_sdt) >= 10
    sdt_char_up = re.search(r"[A-Z]", client_sdt) is None
    sdt_char_spe = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', client_sdt) is None
    sdt_char_low = re.search(r"[a-z]", client_sdt) is None
    if sdt_lenght and sdt_char_low and sdt_char_up and sdt_char_spe:
        return True
    else:
        return False


def check_login(user_name, password):
    temp = Nguoi_dung.query.filter(Nguoi_dung.ten_dang_nhap.__eq__(user_name)).first()
    if temp:
        if temp.mat_khau.__eq__(password):
            return True
        raise Exception("mật khẩu không đúng")
    raise Exception("tên đăng nhập không tồn tại")


def check_birth_day(birth_day):
    temp = datetime.strptime(birth_day, "%Y-%m-%d")
    if temp < datetime.today():
        return True
    else:
        return False


def search_san_bay_by_id(san_bay_id):
    if san_bay_id:
        return San_bay.query.get(san_bay_id)
    else:
        raise Exception("Không có dữ liệu")


def load_lich_bay(chuyen_bay):
    query = []
    lich_bay = Lich_bay.query.all()
    for c in chuyen_bay:
        for lich in lich_bay:
            if lich.chuyen_bay_id == c.id:
                query.append(lich)
    return query


def load_ds_ghe(chuyen_bay_id):
    return Ghe.query.filter(Ghe.Chiec_may_bay_id == chuyen_bay_id).all()


def load_table_ghe(chuyen_bay_id):
    count_ghe = Ghe.query.filter(Ghe.Chiec_may_bay_id == chuyen_bay_id).count()
    ds_ghe = load_ds_ghe(chuyen_bay_id)
    size = int((count_ghe / 3) + 1)
    table = []
    start = 0
    end = 3
    for i in range(size):
        temp = ds_ghe[start:end]
        start = end
        end += 3
        table.append(temp)
    return table
def load_gia_ve_by_chuyen_bay(tuyen_id, hang_ve):
    chuyen = Chuyen_bay.query.filter(Chuyen_bay.tuyen_bay_id == tuyen_id).first()
    price = Ve_may_bay.query.filter(Ve_may_bay.chuyen_bay_id == chuyen.id,
                                    Ve_may_bay.hang_ve.__eq__(hang_ve)).first()
    return price.gia_tien

def load_gia_ve(chuyen_bay):
    query = []
    ve = Ve_may_bay.query.all()
    for c in chuyen_bay:
        for v in ve:
            if Ve_may_bay.chuyen_bay_id == c.id:
                query.append(v)
    return query


