#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Author: Ririkizzu
# Date: 2021/1/1

import requests
import json
import schedule
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

# 初始化个人总积分
contribute_ = xxx


# 获取个人ID和个人总积分
def get_contribute():
    url = "https://security.bytedance.com/user/ajax/auth/get_user_information/"
    headers = {
        # 个人ByteSRC账户登录Cookie
        "Cookie": "sessionid=xxx"
    }
    try:
        r = requests.get(url, headers=headers)
        r_json = json.loads(r.text)
        nick_name = r_json["data"][0]["nick_name"]
        contribute = r_json["data"][0]["contribute"]
        return nick_name, contribute
    except Exception:
        return False


# WebHook地址
webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
# 创建机器人勾选"加签"选项时使用
secret = "xxx"
# 初始化机器人
bot_bytesrc = DingtalkChatbot(webhook, secret)


# 积分增加时发送钉钉提醒
def send_msg(nick_name, contribute, contribute_):
    bot_bytesrc.send_link(title="{}，您的洞审核通过啦！".format(nick_name), text="增加{}分，".format(contribute) + "目前总分{}分".format(
        contribute_), message_url="https://security.bytedance.com/honor/rank/")


# 发生异常时钉钉提醒
def send_err_msg(err_msg):
    bot_bytesrc.send_text(msg=err_msg)


# 若个人总积分增加，发送钉钉Link消息，发生异常，发送异常钉钉提醒
def job():
    global contribute_
    if get_contribute():
        nick_name, contribute = get_contribute()
        if nick_name == "":
            try:
                raise Exception
            except Exception:
                send_err_msg("nick_name为空，检查一下是不是Cookie失效了？")
        if int(contribute) > contribute_:
            contribute = contribute - contribute_
            contribute_ = contribute_ + contribute
            send_msg(nick_name, contribute, contribute_)
    else:
        send_err_msg("连接bytesrc异常，检查一下网络问题？")


# 每5分钟执行一次任务
def main():
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
