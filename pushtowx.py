import requests
from bs4 import BeautifulSoup
import time


def send_notice(content):
    token = "token写这里"
    title = "近期有降雨"
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template=html"
    response = requests.request("GET", url)
    print(response.text)


def dayinfo(day_hour_weather_collect, text_time, text_precipitation) -> str:
    israin = False
    hour_info_set = []
    for onehour_info in day_hour_weather_collect:
        allday_info = onehour_info.getText()
        onehour_info = onehour_info.find_all("div")
        amount_of_precipitation = onehour_info[2].getText()
        if not amount_of_precipitation == " - ":
            israin = True
        hour_info_set.append(
            text_time
            + onehour_info[0].getText()
            + text_precipitation
            + onehour_info[2].getText()
        )

    if israin:
        send_info = ""
        for hour_info in hour_info_set:
            send_info += hour_info + "\n"
            print(hour_info)
        return send_info
    return ""


def get_weather():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    # http://www.nmc.cn/publish/forecast/AZJ/hangzhou.html
    # http://www.nmc.cn/publish/forecast/ABJ/chaoyang.html
    try:
        html_doc = requests.get(
            "http://www.nmc.cn/publish/forecast/ABJ/chaoyang.html", headers
        )
        html_doc.raise_for_status()
        html_doc.encoding = html_doc.apparent_encoding
    except:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "网络异常 5s后重试")
        raise
    soup = BeautifulSoup(html_doc.text, "html.parser")
    hour_weather = soup.find("div", attrs={"class": "hourItems pull-right clearfix"})
    # 今天
    day0_hour_weather = hour_weather.find(
        "div", attrs={"id": "day0", "class": "clearfix pull-left"}
    )
    day0_hour_weather_collect = day0_hour_weather.find_all(
        "div", attrs={"class": "hour3 hbg"}
    )
    msg0 = dayinfo(day0_hour_weather_collect, "今日时间：", "降水：")

    # 明天
    day1_hour_weather = hour_weather.find(
        "div", attrs={"id": "day1", "class": "clearfix pull-left"}
    )
    day1_hour_weather_collect = day1_hour_weather.find_all(
        "div", attrs={"class": "hour3 hbg"}
    )
    msg1 = dayinfo(day1_hour_weather_collect, "明日时间：", "降水：")

    if (not msg0 == "") or (not msg1 == ""):
        send_notice(msg0 + msg1)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "查询正常, 已发送降雨通知, 24小时后继续任务")
        return True
    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "查询正常, 无降雨不通知, 2.5小时后继续任务")
        return False


if __name__ == "__main__":
    while True:
        try:
            israin = get_weather()
        except:
            time.sleep(5)
            continue
        if israin:
            time.sleep(86400)  # 有降雨预报暂停24小时推送
        else:
            time.sleep(9000)  # 无降雨预报2.5小时后继续推送
