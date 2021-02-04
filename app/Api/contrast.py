from flask import Blueprint, make_response, request  # type:request
from flask_cors import CORS  # type: CORS
# from app.Model.models import MeiTuan_Move_Info as MT
from app.Model.models import MeiTuan_Move_Info_V2 as MT
from app.utils.message import response_info
from app.Global import CATEGORIES_ID_DATA, AREA_DATA, BAIYUN_AREA
import pandas as pd  # type: pd
from app.exts import db

contrast = Blueprint("contrast", __name__)
CORS(contrast, supports_credentials=True)

# baiyun = pd.read_excel('../static/baiyunpoi_80.xls')
# 对比
@contrast.route("/test/")
def test():
    def split_addr(data):
        addr = data['CITY'] + data['DISTRICT'] + data['TOWN'] + data['VILLAGE'] + data['STREET'] + data['DOORPN']
        return addr

    addr_list = baiyun.apply(split_addr, axis=1).to_list()
    print(addr_list)
    return response_info(msg='1', data=addr_list)

@contrast.route("/test2/")
def test2():
    return "Hello Flask"
