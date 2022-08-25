# wxpush
## 微信天气消息推送

1.打开https://www.pushplus.plus/
![image](https://user-images.githubusercontent.com/45934872/186588423-7dba8973-815d-407c-acd4-7949bb0dc904.png)

2.获取token 写到send_notice函数token变量上

3.运行pushtowx 会自动爬 http://www.nmc.cn/publish/forecast/ABJ/chaoyang.html 中央气象局

PS：若近两天推送一次降雨预告，那么下一次查询将在24小时后，如果查询近两天没雨，那么下一次查询将在2.5小时后，若网络异常，那么5秒后重试
![image](https://user-images.githubusercontent.com/45934872/186589342-60af45ca-385a-44e8-afd0-9ca6373be417.png)
