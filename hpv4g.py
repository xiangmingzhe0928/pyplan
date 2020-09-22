#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import HTTPError
import datetime
from threading import current_thread
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
import argparse
import logging

LOG_NAME = 'hpv.log'
# disable ssl warnings
requests.packages.urllib3.disable_warnings()

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
    "IP_PROXY": "https://ip.jiangxianli.com/api/proxy_ips",
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
    except Exception as err:
        print(f'URL:{url} error occurred{err}')
        logging.error(f'URL:{url} ERROR:{err}')
        exit(1)
    else:
        res_json = response.json()
        logging.info(f'{url}\n{"-"*5 + "Request" + "-"*5}\n{"-"*5 + "Response" + "-"*5}\n{res_json}\nuseTime:{response.elapsed.total_seconds()}S\n')
        return res_json


def get_vaccine_list(region_code='5101'):
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
    req_param_list = {'offset': '0', 'limit': '10', 'regionCode': region_code}
    res_vaccine = _get(URLS['VACCINE_LIST'], params=req_param_list, headers=REQ_HEADERS, verify=False)
    if '0000' != res_vaccine['code']:
        print(res_vaccine['msg'])
        exit(1)

    datas = res_vaccine['data']
    if not datas:
        print(f'---区域:{region_code}暂无可秒杀疫苗---')
        exit(0)
    return datas


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
    res_json = _get(URLS['USER_INFO'], headers=REQ_HEADERS, verify=False)
    if '0000' == res_json['code']:
        return res_json['data']
    print(f'获取用户信息失败:{res_json}')
    exit(1)


# 秒杀结果标志位
KILL_FLAG = False


def sec_kill_task(req_param, proxy=None):
    """
    执行秒杀操作
    :return:
    """
    global KILL_FLAG
    while not KILL_FLAG:
        '''
        服务器做了频率限制 短时间请求太多返回 “操作频繁” 无法确定是 IP限制还是ID限制
        - 考虑加入ip代理处理IP限制 init_ip_proxy_pool()
        '''
        res_json = _get(URLS['SEC_KILL'], params=req_param, headers=REQ_HEADERS, proxies=proxy, verify=False)
        if res_json['code'] == '0000':
            print(f'{current_thread().name} Kill Success')
            KILL_FLAG = True


def init_ip_proxy_pool(pages=2) -> list:
    """
    填充临时IP代理池。（考虑到秒杀场景瞬时性,提前初始化可用的IP代理 避免秒杀中临时调用API）

    IP代理来源
        1.使用收费的代理商提供
        2.自建IP代理池
            - 爬取免费IP代理
            - 验证IP可用
            - 持久化
            - 定时更新可用IP

    这里直接使用第三方提供的API(避免自建轮子、搭建环境。测试)：https://github.com/jiangxianli/ProxyIpLib
    :return: ip代理池列表
    """
    ip_proxy_res = [
        _get(URLS['IP_PROXY'], params={'page': p, 'country': '中国', 'order_by': 'validated_at'}, verify=False)['data'][
            'data'] for
        p in range(1, pages + 1)]
    return [f'{data["ip"]}:{data["port"]}' for data in list(chain(*ip_proxy_res))]


def run(max_workers=None, region_code=None):
    # 获取疫苗信息(默认选取第一个待秒疫苗)
    vaccines = get_vaccine_list(region_code)
    # 获取秒杀人信息
    user = get_user()
    # 秒杀请求参数
    req_param = {'vaccineIndex': '1', 'seckillId': vaccines[0]['id'], 'linkmanId': user[0]['id'],
                 'idCardNo': user[0]['idCardNo']}
    # 初始化IP代理池
    ip_proxys = init_ip_proxy_pool()
    # 计算秒杀开始剩余毫秒数 startTime - serverNowTime
    _start_time_unix = int(datetime.datetime.strptime(vaccines[0]['startTime'], '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    if _start_time_unix - get_server_time() > 5 * 1000:
        print(f'秒杀还未开始 请在秒杀开始前5秒内执行')
        exit(0)

    # _start_time_unix - get_server_time() 使用本地时间还是服务器时间？
    while _start_time_unix - int(datetime.datetime.now().timestamp() * 1000) > 300:
        pass

    # python3.8 默认max_workers = min(32, os.cpu_count() + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as t:
        ip_proxy_len = len(ip_proxys)
        for i in range(100):
            # 此处并没有使用随机选择代理
            index = i % ip_proxy_len
            t.submit(sec_kill_task, req_param, {'https': None if index == 0 else ip_proxys[index]})


def _get_arguments():
    """
    解析参数
    :return:
    """

    def _valid_int_type(i):
        valid_int = int(i)
        if valid_int < 1:
            raise argparse.ArgumentTypeError(f'invalid int argument:{i}')
        return valid_int

    parser = argparse.ArgumentParser(description='HPV SecKill 疫苗秒杀')
    parser.add_argument('tk', help='名为tk的http header')
    parser.add_argument('cookie', help='http请求cookie')
    parser.add_argument('-mw', '--max_workers', type=_valid_int_type, help='最大线工作线程数 默认使用 min(32, os.cpu_count() + 4)')
    parser.add_argument('-rc', '--region_code', type=int, default='5101', help='区域编码 默认使用成都编码5101')
    parser.add_argument('--log', default='WARNING', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='日志级别 默认WARNING')
    return parser.parse_args()


if __name__ == '__main__':
    args = _get_arguments()

    logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_NAME,
                                                      encoding='utf-8', mode='a+')],
                        format='%(message)s',
                        level=getattr(logging, args.log))
    REQ_HEADERS['tk'] = args.tk
    REQ_HEADERS['Cookie'] = args.cookie
    run(args.max_workers, args.region_code)
