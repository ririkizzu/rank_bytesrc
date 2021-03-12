# rank_bytesrc
ByteSRC漏洞通过钉钉提醒

![](./example.jpg)

### Introduction
每个白帽子肯定都经历过等待漏洞审核的煎熬，尤其是ByteSRC，漏洞审核之后，也不会给白帽子发个反馈信息，只能去平台上一遍一遍刷新，比较浪费时间和精力

偶然间看到[@ohlinge](https://github.com/ohlinge "@ohlinge")师傅的`rank_asrc`项目，感觉挺好用的，按照他的思路，写了一个ByteSRC漏洞审核提醒的脚本，因为邮件提醒可能不够及时，所以改成用钉钉机器人来进行提醒

### Usage
根据自己的设置替换`xxx`
 - 设置ByteSRC登录Cookie
 - 修改钉钉机器人WebHook地址和"加签"
 - 请求频率默认为10分钟一次，可修改：schedule.every(10).minutes.do(job)

Linux命令后台运行
```
nohup python3 rank_bytesrc.py &
```

### Reference
 - https://github.com/ohlinge/rank_asrc
