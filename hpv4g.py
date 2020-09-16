#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import HTTPError
import threading
import datetime

"""
 SecKill HPV
 - 抓取,配置Cookie
 - 获取服务器时间
 - 获取待秒杀疫苗列表
 - 选取秒杀疫苗
 - 计算秒杀开始
 - 多线程并发秒杀
 
"""

URLS = {
    "SERVER_TIME": "https://miaomiao.scmttec.com/seckill/seckill/now2.do",
    "VACCINE_LIST": "https://miaomiao.scmttec.com/seckill/seckill/list.do",
    "USER_INFO": "https://miaomiao.scmttec.com/seckill/linkman/findByUserId.do",
    "SEC_KILL": "https://miaomiao.scmttec.com/seckill/seckill/subscribe.do"
}

REQ_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Referer": "https://servicewechat.com/wxff8cad2e9bf18719/10/page-frame.html",
    "Accept": "application/json, text/plain, */*",
    "Host": "miaomiao.scmttec.com",
    "tk": "",
    "Cookie": ""}


def _get(url, params=None, **kwargs):
    """
    GET请求. 请求返回错误码(4XX,5XX)时抛出异常
    :param url: 请求路径
    :param params: 请求参数
    :param kwargs: 附加信息
    :return: 结果JSON
    """
    try:
        response = requests.get(url, params, **kwargs)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'--------HTTP error occurred--------: {http_err}')
        return None
    except Exception as err:
        print(f'--------Other error occurred--------: {err}')
        return None
    else:
        res_json = response.json();
        print(f'Response:{res_json}')
        return res_json


def get_vaccine_list():
    """
    获取待秒杀疫苗列表
    :return:疫苗列表
        {
          "code": "0000",
          "data": [
            {
              "id": 676,
              "name": "成都市高新区桂溪社区卫生服务中心",
              "imgUrl": "https://adultvacc-1253522668.picgz.myqcloud.com/thematic%20pic/%E6%88%90%E9%83%BD%E5%B8%82%E9%AB%98%E6%96%B0%E5%8C%BA%E6%A1%82%E6%BA%AA%E7%A4%BE%E5%8C%BA%E5%8D%AB%E7%94%9F%E6%9C%8D%E5%8A%A1%E4%B8%AD%E5%BF%83%E5%AE%A3%E4%BC%A0%E5%9B%BE_1544521410544.png?imageView2/1/w/200/format/jpg",
              "vaccineCode": "8803",
              "vaccineName": "九价人乳头瘤病毒疫苗",
              "address": "成都市武侯区昆华路1102号",
              "startTime": "2020-09-16 09:00:00",
              "stock": 1
            },
          ],
          "ok": true,
          "notOk": false
    }
    """
    # 分页查询可秒杀疫苗 regionCode:5101[四川成都区域编码]
    req_param_list = {'offset': '0', 'limit': '10', 'regionCode': '5101'}
    return _get(URLS['VACCINE_LIST'], params=req_param_list, headers=REQ_HEADERS, verify=False)


def get_server_time():
    """
    获取服务器当前时间戳
    秒杀开始时间由服务器控制
    :return: 服务器时间戳
    """
    res_json = _get(URLS['SERVER_TIME'], verify=False)
    return res_json['data']


def get_user():
    """
    获取用户信息(从微信小程序入口 使用微信tk和cookie查询指定用户信息)
    :return: 用户信息
    """
    _get(URLS['USER_INFO'], headers=REQ_HEADERS, verify=False)


# 秒杀结果标志位
KILL_FLAG = False


def sec_kill_task(thread_name):
    """
    执行秒杀操作
    :return:
    """
    print(f'------Thread:{thread_name} start------')
    global KILL_FLAG
    while not KILL_FLAG:
        res_json = _get(URLS['SEC_KILL'], params=req_param, headers=REQ_HEADERS, verify=False)
        if res_json['code'] == '0000':
            print(f'Thread:{thread_name} Kill Success')
            KILL_FLAG = True


class KillThread(threading.Thread):
    """
    秒杀线程
    后续使用线程池
    """

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        sec_kill_task(self.name)


if __name__ == '__main__':
    # 传入Cookie
    REQ_HEADERS['tk'] = 'wxapptoken:10:de185e962abea05b50e4dde9e7558680_d0927647191d344b6999cf28f2ffc04b'
    REQ_HEADERS[
        'Cookie'] = '_xxhm_=%7B%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fic9BcyRDyOIvnjrvBdDBtXAVdFx00GRyl0okTAEgNQ2p8AjJZZuibm7h2wJ2icNbMs5EnyRib9TbtrsWCDj4gPuR3aK6F41icxL6M%2F132%22%2C%22mobile%22%3A%22130****9389%22%2C%22nickName%22%3A%22Min+Jet%22%2C%22sex%22%3A2%7D; _xzkj_=wxapptoken:10:de185e962abea05b50e4dde9e7558680_d0927647191d344b6999cf28f2ffc04b; 8de1=d00b3ed29172b8c4b8'

    # 获取疫苗信息(默认选取第一个待秒疫苗)
    vaccines = get_vaccine_list()['data']
    if len(vaccines) == 0:
        print(f'---暂无可秒杀疫苗---')
        exit(0)

    # 秒杀请求参数
    req_param = {'vaccineIndex': '1',  'linkmanId': 'xx', 'idCardNo': 'xx', 'seckillId': vaccines[0]['id']}

    # 计算秒杀开始剩余毫秒数 startTime - serverNowTime
    _start_time_unix = int(datetime.datetime.strptime(vaccines[0]['startTime'], '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    if _start_time_unix - get_server_time() > 5 * 1000:
        print(f'秒杀还未开始')
        exit(0)

    # _start_time_unix - get_server_time() 使用本地时间还是服务器时间？
    while _start_time_unix - int(datetime.datetime.now().timestamp() * 1000) > 300:
        pass

    thread1 = KillThread('killThread1')
    thread2 = KillThread('killThread2')
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    pass
