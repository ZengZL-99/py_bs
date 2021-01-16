from flask import Blueprint, make_response, request
from flask_cors import CORS
from app.meituan.meituan_move_info import MeiTuan_Move
from app.Model.models import MeiTuan_Move_Info
from app.exts import db
from app.Model.models import User  # type:User
from app.Global import CATEGORIES_ID_DATA, AREA_DATA

api = Blueprint("api", __name__)

CORS(api, supports_credentials=True)


@api.route("/hello")
def hello():
    return "hello"


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
                }
            }
    return


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
        mt_info = MeiTuan_Move_Info.query.all()
        data = []
        for info in mt_info:
            data.append({"name": info.name, "id": info.mid})
        return {"data": data}


@api.route("/test")
def test():
    meituan = MeiTuan_Move_Info(name="火锅店", addr="北京市", areaName="天河", poiId=1101,
                                phone="17817780995", shop_url="http://www.baidu.com", datetime=16000415541)
    db.session.add(meituan)
    db.session.commit()
    return "插入成功"


# 类目数据
@api.route("/categories_data")
def categories():
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
    for i in AREA_DATA:
        area_id = i.get("areaId")
        area_name = i.get("areaName")
        info = {
            "value": area_id,
            "label": area_name,
            "children": []
        }
        for r in i.get("region"):
            region_id = r.get("areaId")
            region_name = r.get("regionName")
            info.get("children").append(
                {
                    "value": region_id,
                    "label": region_name
                }
            )
        data.append(info)
    return {
        "code": 200,
        "data": data
    }


@api.route("/test_user")
def test_user():
    user = User()
    user.name = "www"
    db.session.add(user)
    db.session.commit()
    return "添加成功？"
