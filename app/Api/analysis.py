from flask import Blueprint, make_response, request  # type:request
from flask_cors import CORS  # type: CORS
from app.Model.models import MeiTuan_Move_Info as MT
from app.utils.message import response_info
from app.Global import CATEGORIES_ID_DATA, AREA_DATA, BAIYUN_AREA
import pandas as pd  # type: pd
from app.exts import db

analysis = Blueprint("analysis", __name__)
CORS(analysis, supports_credentials=True)


# 分析每个区域的总数  pie图
@analysis.route("/area_count")
def aly_pie():
    """分析出每个区域"""
    if request.method == "GET":
        db.create_all()
        # query_list = ['龙归镇']
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA))
        result_list = []
        for r in result:
            result_list.append(
                {
                    "地址": r.addr,
                    "店铺名称": r.name,
                    "poiID": r.poiId,
                    "好评数": r.markNumbers,
                    "品牌ID": r.brandId,
                    "品牌名称": r.brandName,
                    "区域名称": r.areaName
                }
            )
        data = pd.DataFrame(result_list)
        df1 = data.groupby(by=["区域名称"])["区域名称"].count().to_dict()
        data = []
        for k, v in df1.items():
            data.append({
                "areaName": k,
                "count": v
            })
        return response_info(msg="1", data=data)
    return response_info(msg="2")


# 分析每个区域的好评平均数
@analysis.route("/area_mark_mean")
def area_mark_mean():
    db.create_all()
    if request.method == "GET":
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA))
        query_list = []
        for r in result:
            query_list.append(
                {
                    "好评数": r.markNumbers,
                    "品牌ID": r.brandId,
                    "品牌名称": r.brandName,
                    "区域名称": r.areaName
                }
            )
        df = pd.DataFrame(query_list)

        def filter_mark(data):
            if data["好评数"] != 0:
                return data

        df = df.apply(filter_mark, axis=1)
        group_area_mark = df.groupby(by=["区域名称"])["好评数"].mean().to_dict()
        data_list = []
        for k, v in group_area_mark.items():
            data_list.append({
                "areaName": k,
                "meanMark": int(v)
            })
        return response_info(msg="1", data=data_list)
    return response_info(msg="2")


# 品牌商家与个体营业的占比
@analysis.route("/aly_brand")
def aly_brand():
    if request.method == "GET":
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA))
        query_list = []
        for r in result:
            query_list.append(
                {
                    "品牌ID": r.brandId,
                    "品牌名称": r.brandName,
                    "区域名称": r.areaName
                }
            )
        df = pd.DataFrame(query_list)

        def filter_brand(data):
            if data["品牌ID"] != 0:
                return 1
            else:
                return data["品牌ID"]

        df["品牌ID"] = df.apply(filter_brand, axis=1)
        group_brand = df.groupby(by=["品牌ID"])["品牌ID"].count()

        return response_info(msg="1")
    return response_info(msg="2")