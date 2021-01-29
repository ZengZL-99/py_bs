from operator import or_
import json
import requests as req
from flask import Blueprint, make_response, request
from flask_cors import CORS
from app.meituan.meituan_move_info import MeiTuan_Move
from app.Model.models import MeiTuan_Move_Info as MT
from app.exts import db
from app.Model.models import User  # type:User
from app.Global import CATEGORIES_ID_DATA, AREA_DATA, BAIYUN_AREA
from app.utils.message import response_info
import random

# from app.utils import props_with
api = Blueprint("api", __name__)

CORS(api, supports_credentials=True)


@api.route("/login", methods=["POST"])
def login():
    info = {
        "data": {
            "token": "admin-token"
        },
        "code": 200
    }
    return make_response((info, 200))


@api.route("/user/info")
def user_info():
    if request.method == "GET":
        token = request.args.get("token")
        if token == "admin-token":
            return {
                "code": 200,
                "data": {  # https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif
                    "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                    "introduction": "I am a super administrator",
                    "name": "Super Admin",
                    "roles": ["admin"]
                },
                "msg": "查询成功"
            }
    return {
        "code": 200,
        "data": None,
        "msg": "查询成功"
    }


@api.route("/crawl_meituan")
def meituan_move():
    if request.method == "GET":
        page = int(request.args.get('page'))
        print(page)
        meituan = MeiTuan_Move(city=20, offset=1, page=int(page))
        meituan.run()
        info = meituan.get_info()
        print(info)
        return {"data": info}


@api.route("/query_mt")
def query_mt():
    if request.method == "GET":
        mt_info = MT.query.all()
        data = []
        for info in mt_info:
            data.append({"name": info.name, "id": info.mid})
        return {"data": data}


# 类目数据
@api.route("/categories_data")
def categories():
    db.create_all()
    data = []
    for i in CATEGORIES_ID_DATA:
        # 判断ID是否为0或者-1 这两个类目为空
        if i.get("id") == 0 or i.get("id") == -1:
            continue
        info = {
            "value": i.get("id"),
            "label": i.get("name"),
        }
        if len(i.get('subcategories')) != 0:
            info.update({"children": []})
            for c in i.get("subcategories"):
                sub_info = {
                    "value": c.get("sub_Id"),
                    "label": c.get("sub_name")
                }
                info.get("children").append(sub_info)
        data.append(info)
    return {
        "code": 200,
        "data": data
    }


# 区域数据
@api.route("/area_data")
def area_data():
    data = []
    info = {
        "value": "全部",
        "label": "全部",
        "children": []
    }
    for i in BAIYUN_AREA:
        info.get("children").append({
            "value": i,
            "label": i
        })
    data.append(info)
    # for i in AREA_DATA:
    #     area_id = i.get("areaId")
    #     area_name = i.get("areaName")
    #     info = {
    #         "value": area_id,
    #         "label": area_name,
    #         "children": []
    #     }
    #     for r in i.get("region"):
    #         # region_id = r.get("areaId")
    #         region_name = r.get("regionName")
    #         info.get("children").append(
    #             {
    #                 "value": region_name,
    #                 "label": region_name
    #             }
    #         )
    #     data.append(info)
    return {
        "code": 200,
        "data": data
    }


# 查询结果
@api.route("/handleSelect")
def handle_select():
    if request.method == "GET":
        query_list = []
        select_dict = dict(request.args)
        print("select_字典:", select_dict)
        for v in select_dict.values():
            query_list.append(v)
        result = MT.query.filter(MT.areaName.in_(query_list)).all()
        result_list = []
        for r in result:
            result_list.append(
                {
                    "name": r.name,
                    "addr": r.addr,
                    "shopUrl": r.shop_url,
                    "poiId": r.poiId,
                }
            )
        return response_info(msg="1", data=result_list)
    return response_info(msg="2")


# 获取经纬度
@api.route("/get_lat_lng")
def get_lat_lng():
    if request.method == "GET":
        query_list = ["嘉禾望岗", "江高镇", "永泰", "白云区", "白云国际机场", "白云大道沿线",
                      "白云绿地中心",
                      "百信广场",
                      "石井"]
        # "罗冲围/金沙洲",
        # "钟落潭",
        # "黄石",
        # "黄边",
        # "龙归镇"]
        result = MT.query.filter(MT.areaName.in_(query_list)).all()
        # result = MT.query.all()
        result_list = {
            "code": 200,
            "info": {
                "errno": 0,
                "message": "成功",
                "result": {
                    "count": 1,
                    "data": [
                        {
                            "bound": []
                        }
                    ]
                }
            }
        }
        for r in result:
            result_list.get("info").get("result").get("data")[0].get("bound").append(
                [str(int(float(r.lng) * 100000)), str(int(float(r.lat) * 100000)), str(random.randint(1, 10))]
            )
            # result_list.append(
            #     {
            #         "geometry": {
            #             "type": 'Point',
            #             "coordinates": [int(float(r.lng) * 100000), int(float(r.lat) * 100000)]
            #         },
            #         "properties": {
            #             "count": 1
            #         }
            #     }
            # )
        return result_list
        # return response_info(msg="1", data=result_list)
    return response_info(msg="2")


@api.route("/get_lat_lng_v2")
def get_lat_lng_v2():
    if request.method == "GET":
        query_list = ["嘉禾望岗", "江高镇", "永泰", "白云区", "白云国际机场", "白云大道沿线",
                      "白云绿地中心",
                      "百信广场",
                      "石井"]
        # "罗冲围/金沙洲",
        # "钟落潭",
        # "黄石",
        # "黄边",
        # "龙归镇"]
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA)).all()
        result_list = []
        for r in result:
            result_list.append(
                {
                    "geometry": {
                        "type": 'Point',
                        "coordinates": [float(r.lng), float(r.lat)]
                    },
                    "properties": {
                        "count": random.randint(1, 40)
                    }
                }
            )
        return response_info(msg="1", data=result_list)


# 把异步请求的数据封装成自己的
@api.route("/result_json")
def result_json():
    if request.method == "GET":
        result_json = req.get("https://mapv.baidu.com/gl/examples/data/chinalocation.json").json()
        return {"data": result_json, "code": 200}


# 把异步请求的数据封装成自己的
@api.route("/beijing")
def beijing():
    if request.method == "GET":
        beijing = req.get("https://mapv.baidu.com/gl/examples/static/beijing.07102610.json").json()
        # print(beijing)
        return {"code": 200, "info": beijing}
