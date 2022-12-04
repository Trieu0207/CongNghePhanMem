from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Enum, Time
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from saleapp import db, app
from enum import Enum as user_enum


class base_model(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Tuyen_bay(base_model):
    __tablename__ = "tuyen_bay"
    ten = Column(String(10), nullable=False)
    diem_di = Column(String(50), nullable=False)
    diem_den = Column(String(50), nullable=False)
    Chuyen_bays = relationship('Chuyen_bay', backref='tuyen_bay', lazy=True)

    def __str__(self):
        return self.ten


class May_bay(base_model):
    __tablename__ = "may_bay"
    ten = Column(String(20), nullable=False)
    loai_may_bay = Column(String(20), nullable=False)
    hang_bay = Column(String(20), nullable=False)
    ghi_chu = Column(String(255))
    Ghes = relationship('Ghe', backref='may_bay', lazy=True)
    Chuyen_bays = relationship('Chuyen_bay', backref='may_bay', lazy=True)

    def __str__(self):
        return self.ten


class San_bay(base_model):
    __tablename__ = "san_bay"
    ten_san_bay = Column(String(50), nullable=False)
    San_bay_trung_gian_s = relationship('San_bay_trung_gian', backref='San_bay', lazy = True)
    # chuyen_bay_s = relationship('Chuyen_bay', backref='San_bay', lazy = True)
    def __str__(self):
        return self.ten_san_bay


class Chuyen_bay(base_model):
    __tablename__ = "chuyen_bay"
    loai_chuyen_bay = Column(String(5), nullable=False)
    trang_thai = Column(String(10), nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey(Tuyen_bay.id), nullable=False)
    Ve_may_bays = relationship('Ve_may_bay', backref='chuyen_bay', lazy=True)
    san_bay_di_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    san_bay_di = relationship('San_bay', foreign_keys='Chuyen_bay.san_bay_di_id')
    san_bay_den_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    san_bay_den = relationship('San_bay', foreign_keys='Chuyen_bay.san_bay_den_id')
    may_bay_id = Column(Integer, ForeignKey(May_bay.id), nullable=False)
    san_bay_trung_gian_s = relationship('San_bay_trung_gian', backref='Chuyen_bay', lazy=True)


class San_bay_trung_gian(base_model):
    __tablename__ = "san_bay_trung_gian"
    san_bay_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    thoi_gian_cho = Column(Time, nullable=False)
    ghi_chu = Column(String(255))

    def __str__(self):
        return San_bay.ten_san_bay


class Ghe(base_model):
    __tablename__ = "ghe"
    ten_ghe = Column(String(10), nullable=False)
    loai_ghe = Column(String(10), nullable=False)
    trang_thai = Column(Boolean, default=False)
    ve_may_bays = relationship('Ve_may_bay', backref='ghe', lazy=True)
    Chiec_may_bay_id = Column(Integer, ForeignKey(May_bay.id), nullable=False)

    def __str__(self):
        return self.ten_ghe


class loai_nguoi_dung(user_enum):
    QT = 1
    NV = 2
    ND = 3


class Nguoi_dung(base_model):
    __tablename__ = "nguoi_dung"
    ho_ten_lot = Column(String(50), nullable=False)
    ten = Column(String(50), nullable=False, unique=True)
    cccd = Column(String(12), nullable=False)
    email = Column(String(50), nullable=False)
    sdt = Column(String(10), nullable=False)
    ten_dang_nhap = Column(String(30), nullable=False)
    mat_khau = Column(String(30), nullable=False)
    avatar = Column(String(100))
    # loai_nguoi_dung = Column(loai_nguoi_dung(user_enum), default= loai_nguoi_dung.ND)
    hoat_dong = Column(Boolean, default=True)
    ngay_dang_ki = Column(DateTime)
    Ve_may_bays = relationship('Ve_may_bay', backref='nguoi_dung', lazy=True)
    Hoa_dons = relationship('Hoa_don', backref='nguoi_dung', lazy=True)

    def __str__(self):
        return self.ten_dang_nhap


class Hoa_don(base_model):
    __tablename__ = "hoa_don"
    thoi_gian_thanh_toan = Column(DateTime, nullable=False)
    so_luong_ve = Column(Integer, nullable=False)
    tong_tien = Column(Float, nullable=False)
    Ve_may_bays = relationship('Ve_may_bay', backref='hoa_don', lazy=True)
    nguoi_thanh_toan = Column(Integer, ForeignKey(Nguoi_dung.id), nullable=False)


class Ve_may_bay(base_model):
    gia_tien = Column(Float, nullable=False)
    hang_ve = Column(String(20), nullable=False)
    Ngay_xuat_ve = Column(DateTime, nullable=False)
    ghe_id = Column(Integer, ForeignKey(Ghe.id), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    nguoi_mua_id = Column(Integer, ForeignKey(Nguoi_dung.id), nullable=False)
    hoa_don_id = Column(Integer, ForeignKey(Hoa_don.id), nullable=False)


with app.app_context():
    if __name__ == '__main__':
        db.create_all()
