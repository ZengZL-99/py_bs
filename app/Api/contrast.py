import os
import time

from flask import Blueprint, make_response, request  # type:request
from flask_cors import CORS  # type: CORS
# from app.Model.models import MeiTuan_Move_Info as MT
from app.Model.models import MeiTuan_Move_Info_V2 as MT
from app.utils.message import response_info
from app.Global import CATEGORIES_ID_DATA, AREA_DATA, BAIYUN_AREA
import pandas as pd  # type: pd
from app.Model.models import QiChaCha as QCC
from app.exts import db
import math
import numpy as np

contrast = Blueprint("contrast", __name__)
CORS(contrast, supports_credentials=True)


@contrast.route("/single_contr")
def single_contrast():
    if request.method == "GET":
        query = request.args.get("single")
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA)).filter(MT.name.like(f"%{query}%"))
        query_list = []
        layer_list = []

        def handle_date(time_stamp):
            time_array = time.localtime(time_stamp)
            other_style_time = time.strftime("%Y-%m-%d", time_array)
            return other_style_time

        for r in result:
            query_list.append(
                {
                    "name": r.name,
                    "addr": r.addr,
                    "date": handle_date(int(r.datetime)),
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


# 商户文件上传
@contrast.route("/uploadBus", methods=["GET", "POST"])
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

        EARTH_RADIUS = 6378.137

        def rad(l):
            return round(float(l), 6) * math.pi / 180.0

        def addr_status(row):  # 计算两个经纬度之间的距离
            if row['lat_y'] == 0 and row['lng_y'] == 0 and row['addr_y'] == '无数据':
                return '00'
            else:
                rad_lat1 = rad(row['lat_x'])
                rad_lat2 = rad(row['lat_y'])
                a = rad(row['lat_x']) - rad(row['lat_y'])
                b = rad(row['lng_x']) - rad(row['lng_y'])
                s = 2 * math.asin(math.sqrt(
                    math.pow(math.sin(a / 2), 2) + math.cos(rad_lat1) * math.cos(rad_lat2) * math.pow(math.sin(b / 2),
                                                                                                      2)))
                s = s * EARTH_RADIUS
                s = (s * 10000) / 10
                print('124214124', s)
                if s > 300:
                    return '10'
                else:
                    return '20'

        rs['status'] = rs.apply(addr_status, axis=1)
        rs_dict = rs.values.tolist()
        data = []
        for k in rs_dict:
            data.append({
                "old_lat": round(float(k[0]), 6),
                "old_lng": round(float(k[1]), 6),
                "old_addr": k[2],
                "name": k[3],
                "new_addr": k[4],
                "new_lat": round(float(k[5]), 6),
                "new_lng": round(float(k[6]), 6),
                "status_code": k[7],
            })
        return response_info(msg="1", data=data)
    return response_info(msg="2")


# 企业文件上传
@contrast.route("/uploadCom", methods=['GET', 'POST'])
def upload_com():
    if request.method == "POST":
        file_obj = request.files['file']  # Flask中获取文件
        file_name = request.form.get("fileName")
        if file_obj is None:
            # 表示没有发送文件
            return response_info(msg="2")
        df = pd.read_excel(request.files['file'])
        up_df = df[['NAME', 'SOCIAL_CREDIT_CODE', 'REGISTER_STATU', 'BY_UPDATE_TIME', 'ADDRESS']]
        up_df.rename(columns={'NAME': 'co_name', 'SOCIAL_CREDIT_CODE': 'social_credit', 'REGISTER_STATU': 'reg_status',
                              'BY_UPDATE_TIME': 'approval_date', 'ADDRESS': 'addr'}, inplace=True)

        def change_time(row):
            date = row['approval_date'].split(" ", 1)
            # time_array = time.strptime(date[0], "%Y-%m-%d")
            # try:
            #     timeStamp = int(time.mktime(time_array))
            # except Exception as e:
            #     print(e)
            #     print(date)
            #     return 10
            # return timeStamp * 1000
            return date[0]

        def change_reg_status(row):
            status = row['reg_status']
            if status == "已开业":
                return "在业"
            return status

        up_df['approval_date'] = up_df.apply(change_time, axis=1)
        up_df['reg_status'] = up_df.apply(change_reg_status, axis=1)
        result = QCC.query.all()
        qcc_df = []
        for r in result:
            qcc_df.append(
                {
                    'co_name': r.coName,
                    'social_credit': r.socialCreditCode,
                    'reg_status': r.regStatus,
                    'approval_date': r.approvalDate,
                    'addr': r.addr,
                }
            )
        qcc_data = pd.DataFrame(qcc_df)

        def handle_change_time(row):
            try:
                time_stamp = int(row['approval_date']) / 1000
            except Exception as e:
                print(e)
                print("row", row['approval_date'])
                return np.nan
            time_array = time.localtime(time_stamp)
            other_style_time = time.strftime("%Y-%m-%d", time_array)
            return other_style_time

        qcc_data['approval_date'] = qcc_data.apply(handle_change_time, axis=1)
        rs = pd.merge(up_df, qcc_data, how='left', on=['social_credit'])
        rs.fillna("——", inplace=True)

        def handle_status(row):
            if row['co_name_y'] == "——" and row['addr_y'] == "——" and row['reg_status_y'] == "——" and row[
                'approval_date_y'] == "——":
                return "00"
            else:
                if row['addr_y'] == row['addr_x']:
                    return '20'
                return '10'

        # TODO: 状态码对应表
        """
            {
                “00”: 本地无数据
                “10”: 本地有数据，但位置以变更
                “20”: 本地有数据，且位置相同
                “01”: 本地有数据，经营状态不一样   （还未实现）
            }
        """

        rs['status_code'] = rs.apply(handle_status, axis=1)
        print(rs)
        result_list = rs.values.tolist()
        data = []
        for i in result_list:
            data.append(
                {
                    "coNameX": str(i[0]),
                    "socialCredit": str(i[1]),
                    "regStatusX": str(i[2]),
                    "approvalDateX": str(i[3]),
                    "addrX": str(i[4]),
                    "coNameY": str(i[5]),
                    "regStatusY": str(i[6]),
                    "approvalDateY": str(i[7]),
                    "addrY": str(i[8]),
                    "statusCode": str(i[9])
                }
            )
        return response_info(msg='1', data=data)
    return response_info(msg='2')
