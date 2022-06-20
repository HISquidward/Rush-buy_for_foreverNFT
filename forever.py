import json
import requests
import threading
import random
import time
from PySide2 import QtCore
from PySide2.QtCore import *

buy_key = 0


class ForeverBuyNft(QtCore.QThread, QtCore.QObject):
    _signal = Signal(str)

    def __init__(self, token, device_id, buy_index, user_index, pay_password, expect_money, buy_model, num=100,
                 daemon=None, msage=None):
        super(ForeverBuyNft, self).__init__()
        self.__is_running = True
        self.daemon = daemon
        self.msage = msage
        self.signal = None
        self.model = buy_model
        self.num = num

        self.name = ""
        self.money = 0
        self.buy_order_code = 0
        self.buy_order_msg = ""
        self.init_order_id = 0
        self.init_id = None

        self.expect_money = expect_money
        self.pay_password = pay_password
        self.buy_index = buy_index  # 首页第几个展示窗
        self.user_index = user_index

        self.threads = []  # 创建线程

        self.order_id = 0
        self.order_id_1 = 0
        self.id_index = 1

        self.product = []  # 所售产品代号列表

        self.sign_url = 'https://api.ddpurse.com/v1/signin'  # 登录网址
        self.loginUrl = 'https://api.ddpurse.com/phoenix/public/nft_intl_get_homepage_banner'  # 页面网址
        self.addr0 = 'https://api.ddpurse.com/phoenix/user_nft/nft_intl_get_user_badge_and_fiat_balance'  #
        self.addr = 'https://api.ddpurse.com/phoenix/user_nft/nft_intl_get_address_with_change'
        self.user_init = 'https://api.ddpurse.com/phoenix/user_nft/nft_intl_get_user_info'  # 购买信息页面

        self.init_buy = 'https://api.ddpurse.com/phoenix/public/nft_intl_get_work_detail'  # 初始化购买页
        self.buy_url = 'https://api.ddpurse.com/phoenix/user_nft/nft_intl_buy_order'  # 购买页
        self.get_buy = 'https://api.ddpurse.com/phoenix/user_nft/nft_intl_get_buy_order_info'  #

        self.pay_url = 'https://api.ddpurse.com/phoenix/user_all/nft_intl_pay_nft_buy_order_with_fiat_account_balance'

        self.headers = {
            'POST /phoenix/public/nft_intl_get_homepage_banner HTTP/1.1'
            'user - agent': 'Dart / 2.14(dart:io)',
            'accept - language': 'zh - CN',
            'client - id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept - encoding': 'gzip',
            'content - length': '0',
            'authorization': token,
            'device - id': device_id,
            'hodt': 'api.ddpurse.com',
            'content - type': 'application/json; charset = utf - 8',
            'app - version': '1.6.9',
        }

        self.init_headers = {
            'POST /phoenix/public/nft_intl_get_work_detail HTTP/1.1'
            'user-agent': 'Dart/2.14 (dart:io)',
            'accept-language': 'zh-CN',
            'client-id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept-encoding': 'gzip',
            'content-length': '78',
            'authorization': token,
            'device-id': device_id,
            'host': 'api.ddpurse.com',
            'content-type': 'application/json; charset=utf-8',
            'app-version': '1.6.9'
        }
        self.buy_headers = {
            'POST /phoenix/user_nft/nft_intl_buy_order HTTP/1.1'
            'user-agent': 'Dart/2.14 (dart:io)',
            'accept-language': 'zh-CN',
            'client-id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept-encoding': 'gzip',
            'content-length': '78',
            'authorization': token,
            'device-id': device_id,
            'host': 'api.ddpurse.com',
            'content-type': 'application/json; charset=utf-8',
            'app-version': '1.6.9'

        }

        self.find_header = {
            'POST / phoenix / user_nft / nft_intl_get_buy_order_info HTTP / 1.1'
            'user - agent': 'Dart / 2.14(dart:io)',
            'accept - language': 'zh - CN',
            'client - id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept - encoding': 'gzip',
            'content - length': '78',
            'authorization': token,
            'device - id': device_id,
            'host': 'api.ddpurse.com',
            'content - type': 'application / json; charset = utf - 8',
            'app - version': '1.6.9'
        }

        self.init_pay_header = {
            'POST / phoenix / user_all / nft_intl_pay_nft_buy_order_with_fiat_account_balance HTTP / 1.1'
            'user - agent': 'Dart / 2.14(dart:io)',
            'accept - language': 'zh - CN',
            'client - id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept - encoding': 'gzip',
            'content - length': 98,
            'authorization': token,
            'device - id':device_id,
            'host': 'api.ddpurse.com',
            'content - type': 'application / json;charset = utf - 8',
            'app - version': '1.6.9'

        }

        self.pay_header = {
            'POST /phoenix/user_all/nft_intl_pay_nft_buy_order_with_fiat_account_balance HTTP/1.1'
            'user - agent': 'Dart / 2.14(dart:io)',
            'accept - language': 'zh - CN',
            'client - id': '13f36a97f0250bc2ee128b572b85faa4',
            'accept - encoding': 'gzip',
            'content - length': '146',
            'authorization': token,
            'device - id': device_id,
            'host': 'api.ddpurse.com',
            'content - type': 'application / json; charset = utf - 8',
            'app - version': '1.6.9'
        }

        self.session = requests.session()  # 创建会话

    def __del__(self):
        self.wait()

    def terminate(self):
        self.__is_running = False

    def get_homepage_banner(self):
        request = self.session.post(url=self.loginUrl, headers=self.headers)  # 请求首页信息
        id_1 = json.loads(request.text)
        # print(id_1)
        self.name = id_1["data"]["banners"][self.buy_index]["title"]
        id_1 = id_1["data"]["banners"][self.buy_index]["link"]
        id_1 = id_1.replace("foreverrealm://nft_detail?id=", "")

        for i in range(1, self.num):
            self.product.append(id_1 + "_" + str(i))

        self._signal.emit(id_1)  # 取得商品id

    def get_work_detail(self):
        self.id_index = random.randint(15, 98)
        data = {
            "id": self.product[self.id_index]
        }
        data = json.dumps(data)

        response = self.session.post(url=self.init_buy, data=data, headers=self.init_headers)  # 获得商品id
        response3 = json.loads(response.text)
        # print(response3)
        # print(response3["data"]["nft_items"][buy_index]["price"]["money"])  # 取得商品售价
        # print(response3)

        self.money = float(response3["data"]["nft_items"][0]["price"]["money"])  # 取得商品名称
        self.order_id = response3["data"]["nft_items"][0]["order_id"]  # 取得商品id

    def intl_buy_order(self):
        buy_data = {"id": self.order_id,
                    "user_index": self.user_index,
                    "payment_method": 1}
        buy_data = json.dumps(buy_data)
        # print(self.order_id)
        # print(self.user_index)
        # print(buy_data)

        response = self.session.post(url=self.buy_url, data=buy_data, headers=self.buy_headers)  # 取命令id
        response4 = json.loads(response.text)
        self._signal.emit(response4)
        print(response4)
        if response4["code"] == 0:
            self.order_id_1 = response4["data"]["order_id"]
            self.buy_order_code = response4["code"]
            self.buy_order_msg = response4["msg"]

            self.init_order_id = True
            self.msage = self.buy_order_msg
            self._signal.emit(self.msage)
        else:
            self.init_order_id = False
            self.msage = response4
            self._signal.emit(self.msage)

            # self.terminate()  # 结束线程

    def get_buy_order_info(self):
        if self.init_order_id is True:
            data1 = {
                "order_id": self.order_id_1,
                "user_index": self.user_index,
                "ignore_fee": "true"
            }
            data1 = json.dumps(data1)

            response = self.session.post(url=self.buy_url, data=data1, headers=self.find_header)
            response5 = json.loads(response.text)

            if response5["code"] == 0:
                self._signal.emit(response5)
                self._signal.emit("成功下单")
                self.init_order_id = True
            else:
                self._signal.emit(response5["msg"])
                print(response5["msg"])
                self.init_order_id = False

        else:
            self.init_order_id = False

    def init_pay_nft_buy_order(self):
        if self.init_order_id is True:
            init_pay_data = {"id": self.order_id_1,
                             "payment_method": 3,
                             "need_save": "true",
                             "need_sign": "false",
                             "need_seed": "true"
                             }
            init_pay_data = json.dumps(init_pay_data)
            response = self.session.post(url=self.pay_url, data=init_pay_data, headers=self.init_buy)
            response6 = json.loads(response.text)
            self._signal.emit(response6)

            self.init_order_id = True
            self.terminate()
        else:
            self._signal.emit("下单异常")
            self.init_order_id = False
            self.terminate()

    def pay_nft_buy_order(self):
        if self.init_order_id is True:
            pay_data = {"id": self.order_id_1,
                        "payment_method": 3,
                        "need_save": "true",
                        "need_sign": "false",
                        "need_seed": "true",
                        "security_params": {"payment_password": self.pay_password}
                        }
            pay_data = json.dumps(pay_data)
            response = self.session.post(url=self.pay_url, data=pay_data, headers=self.pay_header)
            response5 = response.text
            self._signal.emit(response5)

            self.init_order_id = False
            self.terminate()
        else:
            self._signal.emit("下单异常")
            self.init_order_id = False
            self.terminate()

    def run(self):
        # if self.comboBox_4.currentText() == "无":
        #     self.init_id = self.textEdit.toPlainText()
        #     for i in range(1, 100):
        #         self.product.append(self.init_id + "_" + str(i))
        # else:
        self.get_homepage_banner()

        while self.__is_running:
            self.get_work_detail()

            if self.money < self.expect_money and self.buy_order_code == 0:
                data1 = "准备购买" + self.name + "#" + str(self.id_index) + "/价格为" + str(self.money)
                self._signal.emit(data1)

                if self.model == 0:
                    self.intl_buy_order()
                    self._signal.emit("测试购买模式通过！")
                    self.terminate()

                if self.model == 1:
                    self.intl_buy_order()
                    self.get_buy_order_info()
                    print("请手动付款")
                    self._signal.emit("请手动付款")
                    self.terminate()
                elif self.model == 2:
                    self.intl_buy_order()
                    if self.init_order_id is True:
                        self.get_buy_order_info()
                        if self.init_order_id is True:
                            self.init_pay_nft_buy_order()
                            time.sleep(1)
                            self.pay_nft_buy_order()
                            print("自动付款")
                            self.terminate()
                        else:
                            print("下单出错")
                            self._signal.emit("下单出错")
                            self.terminate()
                    else:
                        print("订单信息出错")
                        self._signal.emit("订单信息出错")
                        self.terminate()
            else:
                data = "#   " + str(self.id_index) + self.name + "/" + str(self.money) + "价格不符"
                self._signal.emit(data)


def get_detail(buy_index, token, device_id):
    url = 'https://api.ddpurse.com/phoenix/public/nft_intl_get_homepage_banner'  # 页面网址
    headers = {
        'POST /phoenix/public/nft_intl_get_homepage_banner HTTP/1.1'
        'user - agent': 'Dart / 2.14(dart:io)',
        'accept - language': 'zh - CN',
        'client - id': '13f36a97f0250bc2ee128b572b85faa4',
        'accept - encoding': 'gzip',
        'content - length': '0',
        'authorization': token,
        'device - id': device_id,
        'hodt': 'api.ddpurse.com',
        'content - type': 'application/json; charset = utf - 8',
        'app - version': '1.5.5',
    }
    session = requests.session()
    request = session.post(url=url, headers=headers)  # 请求首页信息
    id_1 = json.loads(request.text)
    return id_1["data"]["banners"][buy_index]["title"]


def create_thread(buy_index, password, token, device_id, user_index, expect_money, msage, thread_num=5, model=0):
    threads = []
    for i in range(1, thread_num):
        t = ForeverBuyNft(buy_index=buy_index, pay_password=password,
                          token=token, device_id=device_id,
                          user_index=user_index, expect_money=expect_money, daemon=False, msage=msage, model=model)
        threads.append(t)
        # time.sleep(0.1)
    return threads


def start_threads(threads):
    for thread in threads:
        thread.start()
        # time.sleep(1)


if __name__ == "__main__":
    buy_index_ii = 2
    user_index_ii = 1650388318539
    device_id_ii = 'f40597048a7ee04f'
    token_ii = 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIxM2YzNmE5N2YwMjUwYmMyZWUxMjhiNTcyYjg1ZmFhNCIsImV4cCI6MTY1MDk3MjA1NSwianRpIjoiMTUxODg4MjgwODU2ODc1ODI3MiIsInN1YiI6IjE1MDczNDQxODI5OTMxODI3MjAiLCJzY29wZSI6InVzZXIuYWxsIn0.HLzymoBgN5gibXodvThWaFdyGeIY9fj3K7BzJ3BaJ8676myGqkdbhNTNYmXwPG_TS17ZtMnWcp9ZdYSvXBPihg'
    buy_expect_money = 50.0
    pass_word = '065732'

    model = input("0.测试模式；1.抢购模式")
    token_ii = input("请输入token：")
    start = input("请按回车开始启动......")

    a = None

    many_threads = create_thread(buy_index=buy_index_ii, password=pass_word,
                                 token=token_ii, device_id=device_id_ii,
                                 user_index=user_index_ii, expect_money=buy_expect_money, msage=a)
    start_threads(many_threads)

