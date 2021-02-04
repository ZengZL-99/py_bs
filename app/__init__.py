import pymysql
from flask import Flask
from app.Api.api import api
from settings import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from app.exts import db
from app.Api.analysis import analysis
from app.Api.contrast import contrast

def create_app():
    app = Flask(__name__)
    # db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='test',
    #                      charset='utf8')  # 连接数据库
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(analysis, url_prefix="/aly")
    app.register_blueprint(contrast, url_prefix='/cont')
    # app.static_url_path("../static")
    app.config.from_object(DevelopmentConfig())
    db.init_app(app)

    return app
