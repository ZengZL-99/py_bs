# from sqlalchemy import Column, Integer, String
from app.exts import db  # type:db


class MeiTuan_Move_Info(db.Model):
    __tablename__ = "meituan_move_v_1.0"
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    addr = db.Column(db.String(200), nullable=False)
    areaName = db.Column(db.String(100), nullable=False)
    poiId = db.Column(db.Integer, unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    shop_url = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.Float, nullable=False)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
