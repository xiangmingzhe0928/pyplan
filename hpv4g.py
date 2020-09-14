#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import HTTPError

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
    :param kwargs: 附加信心
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
    """
    # 分页查询可秒杀疫苗 regionCode:5101[四川成都区域编码]
    req_param = {'offset': '0', 'limit': '10', 'regionCode': '5101'}
    _get(URLS['VACCINE_LIST'], params=req_param, headers=REQ_HEADERS, verify=False)


def get_user():
    """
    获取用户信息(从微信小程序入口 使用微信tk和cookie查询指定用户信息)
    :return: 用户信息
    """
    _get(URLS['USER_INFO'], headers=REQ_HEADERS, verify=False)


def sec_kill():
    """
    执行秒杀操作
    :return:
    """
    req_param = {'seckillId': '676', 'vaccineIndex': '1', 'linkmanId': 'xx', 'idCardNo': 'xx'}
    _get(URLS['SEC_KILL'], params=req_param, headers=REQ_HEADERS, verify=False)


if __name__ == '__main__':
    # 传入Cookie
    REQ_HEADERS['tk'] = 'wxapptoken:10:de185e962abea05b50e4dde9e7558680_52a48bbf99cd9aff745339e6d94f57e9'
    REQ_HEADERS[
        'Cookie'] = '_xxhm_=%7B%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fic9BcyRDyOIvnjrvBdDBtXAVdFx00GRyl0okTAEgNQ2p8AjJZZuibm7h2wJ2icNbMs5EnyRib9TbtrsWCDj4gPuR3aK6F41icxL6M%2F132%22%2C%22mobile%22%3A%22130****9389%22%2C%22nickName%22%3A%22Min+Jet%22%2C%22sex%22%3A2%7D; _xzkj_=wxapptoken:10:de185e962abea05b50e4dde9e7558680_52a48bbf99cd9aff745339e6d94f57e9; 8de1=52850933d3ba5e1777'
    # sec_kill()
    pass
