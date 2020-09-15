#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

url='https://oapi.dingtalk.com/robot/send?access_token=xxx'

def send_msg(msg):
    """
    发送消息的函数，这里使用阿里的钉钉
    :param msg: 要发送的消息
    :return: 200 or False
    """
    program = {"msgtype": "text", "text": {"content": msg}, }
    headers = {'Content-Type': 'application/json'}
    try:
        f = requests.post(url, data=json.dumps(program), headers=headers)
    except Exception as e:
        return False
    return f.status_code

info="请审批工单"

send_msg(info)