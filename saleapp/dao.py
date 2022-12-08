from saleapp import app, db
from saleapp.models import Tuyen_bay, Chuyen_bay
from sqlalchemy import or_


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


def load_chuyen_bay_by_tuyen_bay_id(tuyen_bay_id):
     return Chuyen_bay.query.filter(Chuyen_bay.tuyen_bay_id == tuyen_bay_id)
