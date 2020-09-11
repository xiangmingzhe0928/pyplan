#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests

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
    "SEC_KILL": "https://miaomiao.scmttec.com/seckill/seckill/subscribe.do"
}

REQ_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Referer": "https://servicewechat.com/wxff8cad2e9bf18719/10/page-frame.html",
    "Accept": "application/json, text/plain, */*",
    "Host": "miaomiao.scmttec.com",
    "tk": "",
    "Cookie": ""}


def get_vaccine_list():
    """
    获取待秒杀疫苗列表
    :return:
    """
    pass


def sec_kill():
    """
    执行秒杀操作
    :return:
    """
    req_param = {'seckillId': '676', 'vaccineIndex': '1', 'linkmanId': 'xx', 'idCardNo': 'xx'}
    res = requests.get(URLS['SEC_KILL'], params=req_param, headers=REQ_HEADERS, verify=False)
    if res.status_code == requests.codes.ok:
        print(res.json())
    else:
        print('error')
        exit(1)


if __name__ == '__main__':
    # 传入Cookie
    # REQ_HEADERS['tk'] = 'wxapptoken:10:de185e962abea05b50e4dde9e7558680_79f31983921841920f139c4cfa447374'
    # REQ_HEADERS[
    #     'Cookie'] = '_xxhm_=%7B%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fic9BcyRDyOIvnjrvBdDBtXAVdFx00GRyl0okTAEgNQ2p8AjJZZuibm7h2wJ2icNbMs5EnyRib9TbtrsWCDj4gPuR3aK6F41icxL6M%2F132%22%2C%22mobile%22%3A%22130****9389%22%2C%22nickName%22%3A%22Min+Jet%22%2C%22sex%22%3A2%7D; _xzkj_=wxapptoken:10:de185e962abea05b50e4dde9e7558680_79f31983921841920f139c4cfa447374; 8de1=974a587030bfe2d777'
    # sec_kill()

    pass
