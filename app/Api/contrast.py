import os

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

    # addr_list = baiyun.apply(split_addr, axis=1).to_list()
    # print(addr_list)
    return response_info(msg='1')


@contrast.route("/test2/")
def test2():
    return "Hello Flask"


@contrast.route("/single_contr")
def single_contrast():
    if request.method == "GET":
        query = request.args.get("single")
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA)).filter(MT.name.like(f"%{query}%"))
        query_list = []
        layer_list = [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lng), float(lat)]
                },
                "size": 30,
                "color": "red"
            }
        ]
        for r in result:
            query_list.append(
                {
                    "name": r.name,
                    "addr": r.addr,
                    "date": r.datetime,
                    "areaName": r.areaName,
                }
            )
            layer_list.append(
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(r.lng), float(r.lat)]
                    },
                    "size": 10,
                    "color": "green"
                }
            )
        return response_info(msg="1", data={"query_list": query_list, "layer_list": layer_list})
    return response_info(msg="2")


# 测试文件上传
@contrast.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file_obj = request.files['file']  # Flask中获取文件
        file_name = request.form.get("fileName")
        df = pd.read_excel(request.files['file'])
        up_df = df[['LATITUDE', 'LONGITUDE', 'LOCATADDRESS', 'COMPANYNAME']]
        up_df.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lng', 'LOCATADDRESS': 'addr', 'COMPANYNAME': 'name'},
                     inplace=True)
        # print(up_df)
        if file_obj is None:
            # 表示没有发送文件
            return response_info(msg="2")
        # 保存文件
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA))
        query_list = []
        for r in result:
            query_list.append(
                {
                    "name": r.name,
                    "addr": r.addr,
                    "lat": r.lat,
                    "lng": r.lng
                }
            )
        mt_df = pd.DataFrame(query_list)
        # print(mt_df)
        rs = pd.merge(up_df, mt_df, how='left', on=['name'])  # 根据字段name 来筛选
        rs['addr_x'].fillna('无数据', inplace=True)
        rs['addr_y'].fillna('无数据', inplace=True)
        rs.fillna(0, inplace=True)
        rs_dict = rs.values.tolist()
        data = []
        for k in rs_dict:
            data.append({
                "old_lat": round(float(k[0]), 6),
                "old_lng": round(float(k[1]), 6),
                "old_addr": str(k[2]),
                "name": str(k[3]),
                "new_addr": str(k[4]),
                "new_lat": round(float(k[5]), 6),
                "new_lng": round(float(k[6]), 6)
            })
        print("datatatatatatrata", data)
        return response_info(msg="1", data=data)
    return response_info(msg="2")
