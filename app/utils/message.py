# return 回去的规范

msg_list = {
    "1": "成功请求",
    "2": "请求失败"
}


def response_info(msg="2", data=None, code=200):
    """
    规范化返回参数
    :param data: List
    :param msg: Str
    :param code: Int
    :return:
    """
    return {
        "code": int(code),
        "data": data,
        "msg": msg_list.get(str(msg))
    }