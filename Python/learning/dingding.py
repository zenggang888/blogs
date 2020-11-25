#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

url='https://oapi.dingtalk.com/robot/send?access_token=xxx'

#发送普通字符串消息
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


#发送markdown消息
def send_markdown_msg():
    headers = {"Content-Type": "application/json"}

    # 消息类型和数据格式参照钉钉开发文档
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "apk下载",
            "text": "# 这是安卓测试版本 \n ![img](https://xxx.oss-cn-hangzhou.aliyuncs.com/photos/xxx.jpg)"
        }
    }
    r = requests.post(url = dingtalk_url, data=json.dumps(data), headers=headers)

info="请审批工单"

send_msg(info)
