# from sqlalchemy import Column, Integer, String
from app.exts import db  # type:db


class MeiTuan_Move_Info(db.Model):
    __tablename__ = "meituan_move_info"
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    addr = db.Column(db.String(255), nullable=False)
    areaName = db.Column(db.String(100), nullable=False)
    areaId = db.Column(db.Integer, nullable=False)
    poiId = db.Column(db.Integer, unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    shop_url = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.Float, nullable=False)
    lat = db.Column(db.DECIMAL(9, 6), nullable=False)
    lng = db.Column(db.DECIMAL(9, 6), nullable=False)
    markNumbers = db.Column(db.Integer, nullable=False)
    mallId = db.Column(db.Integer, nullable=False)
    brandId = db.Column(db.Integer, nullable=False)
    brandName = db.Column(db.String(255))


class MeiTuan_Move_Info_V2(db.Model):
    __tablename__ = "meituan_move_info_v2"
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    addr = db.Column(db.String(255), nullable=False)
    areaName = db.Column(db.String(100), nullable=False)
    areaId = db.Column(db.Integer, nullable=False)
    poiId = db.Column(db.Integer, unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    shop_url = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.Float, nullable=False)
    lat = db.Column(db.DECIMAL(9, 6), nullable=False)
    lng = db.Column(db.DECIMAL(9, 6), nullable=False)
    markNumbers = db.Column(db.Integer, nullable=False)
    mallId = db.Column(db.Integer, nullable=False)
    brandId = db.Column(db.Integer, nullable=False)
    brandName = db.Column(db.String(255), nullable=False)
    avgprice = db.Column(db.String(255), nullable=False)
    avgscore = db.Column(db.String(255), nullable=False)
    cateName = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))


class Baiyun(db.Model):
    ___tablename__ = "baiyun"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)