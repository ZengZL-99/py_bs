import random
import time
from datetime import datetime

import pymysql
import requests

"""
url关键字段说明
:limit: 获取的条数
::
"""


class MeiTuan_Move():
    def __init__(self, city, offset, page):
        self.url = ""
        self.city = city
        self.offset = offset
        self.proxies_list = []
        self.ip_url = "http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=0&city=0&yys=0&port=1&pack=133181&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions="
        self.page = page
        self.data_list = []
        self.db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='test',
                                  charset='utf8')  # 连接数据库
        self.cursor = self.db.cursor()  # 创建游标
        self.All_Data = []

    def set_ua(self):
        """
        手机User-Agent大全
        :type: Dict
        :return: User-Agent
        """
        ua_list = [
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)"},
            {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36"},
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN"},
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1"},
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; MI 6 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)"},
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)"},
            {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 UWS/2.12.1.18 Mobile Safari/537.36 AliApp(TB/7.5.4) UCBS/2.11.1.1 WindVane/8.3.0 720X1280"}
        ]
        return random.choice(ua_list)

    # 获得IP
    def get_ip(self):
        """
        获取代理IP列表
        :return: append => proxies_list
        """
        req = requests.get(self.ip_url, headers=self.set_ua()).json()
        for i in req.get('data'):
            ip = i.get('ip')
            port = i.get('port')
            proxies = {'http': f'{ip}:{port}',
                       'https': f'{ip}:{port}'
                       }
            self.proxies_list.append(proxies)

    # 设置IP
    def set_ip(self):
        """
        设置代理IP
        :type: Dict
        :return: proxies
        """
        proxies = random.choice(self.proxies_list)
        return proxies

    # 插入数据 SQL
    def install_sql(self, name, addr, areaName, areaId, poiId, phone, shop_url, datetime):
        sql = f"""INSERT INTO meituan_move_info(
             name, addr, areaName, areaId, poiId, phone, shop_url, datetime
             )
             VALUES ('{name}', '{addr}', '{areaName}', {int(areaId)}, {int(poiId)}, '{phone}', '{shop_url}', '{datetime}')"""
        try:
            self.cursor.execute(sql)  # 执行sql语句
            self.db.commit()  # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            print("报错")
            self.db.rollback()

    # 获取页面信息
    def get_response(self, url):
        response = requests.get(url, headers=self.set_ua(), proxies=self.set_ip())
        number = 0
        while True:
            try:
                info_list = response.json().get('data')
                ct_pois = response.json().get('ct_pois')
                if info_list:
                    break
                else:
                    number += 1
                    if number >= 10:
                        return None
                    time.sleep(5)
                    print("get_response----else 当前的number", number)
                    response = requests.get(url, headers=self.set_ua(), proxies=self.set_ip())
                # self.data_list.append(response.json().get("data"))
            except:
                number += 1
                if number >= 10:
                    print("get_response 退出")
                    return None
                time.sleep(5)
                print("get_response---except 当前的number", number)
                response = requests.get(url, headers=self.set_ua(), proxies=self.set_ip())
        item_list = []
        for i in range(len(info_list)):
            name = info_list[i].get('poi').get('name')  # 店铺名称
            addr = info_list[i].get('poi').get('addr')  # 店铺地址
            poiId = info_list[i].get('poi').get('poiid')  # poiid 店铺唯一ID
            areaId = info_list[i].get('poi').get('areaId')  # 所属片区ID
            areaName = info_list[i].get('poi').get('areaName')  # 所属片区名称
            phone = info_list[i].get('poi').get('phone')  # 联系号码
            shop_url = f"http://meishi.meituan.com/i/poi/{ct_pois[i].get('poiid')}?ct_poi={ct_pois[i].get('ct_poi')}"
            #  http://meishi.meituan.com/i/poi/160574797?ct_poi=142862485609920712920077335036110671393_a160574797_c0_e5474727917660840589
            item = {
                "name": name,
                "addr": addr,
                "areaName": areaName,
                "areaId": areaId,
                "poiId": poiId,
                "phone": phone if phone else '00000000',
                "shop_url": shop_url
            }
            item_list.append(item)
            self.All_Data.append(item)
        # print(len(item_list))
        return item_list

    def get_info(self):
        return self.All_Data

    def run(self):
        number = 0
        self.get_ip()
        print(self.proxies_list)
        for i in range(0, self.page):
            print(f"正在爬取第{i + 1}页")
            self.url = f"http://api.meituan.com/group/v4/deal/select/city/{self.city}/cate/1?sort=solds&hasGroup=true&mpt_cate1=1&offset={int(self.offset) + (int(i) * 25)}&limit=25"
            # print(self.url)
            while True:
                try:
                    time.sleep(random.randint(2, 4))
                    install_info = self.get_response(self.url)
                    break
                except:
                    number += 1
                    print("run---except 当前的number", number)
                    if number >= 10:
                        print("run 退出")
                        return None
            if install_info:
                for info in install_info:
                    date = datetime.now().timestamp()
                    self.install_sql(info.get('name'), info.get('addr'), info.get('areaName'),
                                     info.get('areaId'), info.get('poiId'), info.get('phone'), info.get('shop_url'),
                                     date
                                     )


# if __name__ == '__main__':
#     """
#     一页15条 page=10 ====>  150条信息
#     """
#     meituan = MeiTuan_Move(city=20, offset=1, page=100)
#     meituan.run()
#     # poiId_list = []
