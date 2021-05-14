# Author: Ririkizzu
# Date: 2021/1/1

import requests
import json
import schedule
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

# 初始化个人总积分
contribute_ = 0
# 设置登录ByteSRC的身份信息
sessionid = "xxx"
# WebHook地址
webhook = "xxx"
# 创建机器人勾选"加签"选项时使用
secret = "xxx"


def job():
    url = "https://src.bytedance.com/user/ajax/auth/get_user_information/"
    headers = {
        "Cookie": "sessionid=" + sessionid
    }
    try:
        r = requests.get(url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json["status"]
        if status == "ok":
            global contribute_
            nick_name = r_json["data"][0]["nick_name"]
            contribute = r_json["data"][0]["contribute"]
            if int(contribute) > contribute_:
                contribute = contribute - contribute_
                contribute_ = contribute_ + contribute
                send_msg(nick_name, contribute, contribute_)
        else:
            send_err_msg("Cookie已过期，请重新登录。")
    except Exception:
        send_err_msg("连接异常，检查网络问题。")


# 初始化机器人
bot_bytesrc = DingtalkChatbot(webhook, secret)


# 积分增加时发送钉钉提醒
def send_msg(nick_name, contribute, contribute_):
    bot_bytesrc.send_link(title="{}，您的洞审核通过啦！".format(nick_name), text="增加{}分，".format(contribute) + "目前总分{}分".format(
        contribute_), message_url="https://src.bytedance.com/honor/rank/")


# 发生异常时钉钉提醒
def send_err_msg(err_msg):
    bot_bytesrc.send_text(msg=err_msg)


# 每10分钟执行一次任务
def main():
    job()
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
