import sys
import requests
import random
import config
import os
from time import localtime
from time import tzset
from datetime import datetime, date
from zhdate import ZhDate
import template
import json


# 获取应用名字
def get_agent_name(config_data, access_token):
    url = "https://qyapi.weixin.qq.com/cgi-bin/agent/get?access_token={}&agentid={}".format(access_token,
                                                                                            config_data["agent_id"])
    r = requests.get(url).json()
    if r["errcode"] == 0:
        agent_name = r["name"]
    else:
        agent_name = ""
    return agent_name


# 处理详情页
def handle_html(url_data, agent_name, year):
    with open(os.path.join(os.path.dirname(__file__), "show.html"), 'r', encoding='utf-8') as f:
        html = f.read()
    a = agent_name
    html = html.replace("<&a&>", a)
    y = year
    html = html.replace("<&y&>", y)
    p = url_data.get("picurl")
    t = url_data.get("title")
    c = url_data.get("content")
    if p and p != "none" and p != "None":
        html = html.replace(".pic{display:none}", "").replace("<&p&>", p)
    if t and t != "none" and t != "None":
        t = t.replace("\\n", "<br/>")
        html = html.replace(".title{display:none}", "").replace("<&t&>", t)
    if c and c != "none" and c != "None":
        c = c.replace("\\n", "<br/>")
        html = html.replace(".content{display:none}", "").replace("<&c&>", c)
    return html


def get_region_data(config_data, weather_type):
    # 获取所有地区数据
    region_data = {}
    for k, v in config_data.items():
        if k[0:6] == "region":
            # 传入地区获取天气信息
            region = v
            id = k[6:]
            weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal = get_weather(
                region, config_data, weather_type)
            if weather == "地区数据找不到":
                yq_data = "地区数据找不到"
            elif weather == "未配置和风天气key":
                yq_data = "未配置和风天气key"
            elif weather == "未配置和风天气key或key配置错误":
                yq_data = "未配置和风天气key或key配置错误"
            else:
                # 获取疫情数据
                yq_data = yq(region, config_data, weather_type)
            region_data[k] = region
            region_data["weather{}".format(id)] = weather
            region_data["max_temp{}".format(id)] = max_temp
            region_data["min_temp{}".format(id)] = min_temp
            region_data["temp{}".format(id)] = temp
            region_data["wind_dir{}".format(id)] = wind_dir
            region_data["sunrise{}".format(id)] = sunrise
            region_data["sunset{}".format(id)] = sunset
            region_data["category{}".format(id)] = category
            region_data["pm2p5{}".format(id)] = pm2p5
            region_data["proposal{}".format(id)] = proposal
            region_data["yq{}".format(id)] = yq_data
    return region_data


def get_image_url():
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Content-type': 'application/x-www-form-urlencoded'

    }
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8-sig'
    image_url = "https://cn.bing.com" + json.loads(r.text)["images"][0]["url"]
    return image_url


def get_tianhang(config_data):
    url = "https://api.vvhan.com/api/reping"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.get(url, headers=headers).json()
    name =response["data"]["name"]
    auther = response["data"]["auther"]
    picUrl = response["data"]["picUrl"]
    avatarUrl = response["data"]["avatarUrl"]
    content = response["data"]["content"]
    return name, auther,picUrl,avatarUrl,content

def get_horoscope(config_data):
    # 获取所有星座数据
    horoscope_data = {}
    for k, v in config_data.items():
        if k[0:9] == "horoscope":
            try:
                key = config_data["tian_api"]
                url = "http://api.tianapi.com/star/index?key={}&astro={}".format(key, v)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Content-type': 'application/x-www-form-urlencoded'

                }
                response = requests.get(url, headers=headers).json()
                if response["code"] == 200:
                    horoscope = response["newslist"][-1]["content"]
                    horoscope = horoscope.split("。")[0]
                else:
                    horoscope = response["msg"]
            except KeyError:
                horoscope = "未配置天行数据key"
            horoscope_data[k] = horoscope
    return horoscope_data


def yq(region, config_data, weather_type):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
    }
    if weather_type == 2:
        try:
            key = config_data["tian_api"]
        except KeyError:
            data = "未配置天行数据key"
            return data
        region_url = "http://api.tianapi.com/citylookup/index?key={}&area={}".format(key, region)
        response = requests.get(region_url, headers=headers).json()
        if response["code"] == 200:
            city = response["newslist"][0]["citycn"]
            if city in ["台北", "高雄", "台中", "台湾"]:
                city = "台湾"
        else:
            return response["msg"]
    else:
        key = config_data["weather_key"]
        url = "https://geoapi.qweather.com/v2/city/lookup?key={}&location={}".format(key, region)
        r = requests.get(url).json()
        if r["code"] == "200":
            city = r["location"][0]["adm2"]
            if region in ["台北", "高雄", "台中", "台湾"]:
                city = "台湾"
        else:
            return ""
    response = requests.get('https://covid.myquark.cn/quark/covid/data?city={}'.format(city), headers=headers).json()
    if city in ["北京", "上海", "天津", "重庆", "香港", "澳门", "台湾"]:
        city_data = response["provinceData"]
    else:
        city_data = response["cityData"]
    try:
        sure_new_loc = "昨日新增：{}".format(city_data["sure_new_loc"])
        sure_new_hid = "昨日无症状：{}".format(city_data["sure_new_hid"])
        present = "现有确诊：{}".format(city_data["present"])
        danger = "中/高风险区：{}/{}".format(city_data["danger"]["1"], city_data["danger"]["2"])
        statistics_time = response["time"]
        yq_data = "{}疫情数据\n{}\n{}\n{}\n{}\n{}".format(city, sure_new_loc, sure_new_hid, present, danger,
                                                      statistics_time)
    except TypeError:
        yq_data = ""
    return yq_data


def get_commemoration_day(today, commemoration_day):
    # 获取纪念日的日期格式
    commemoration_year = int(commemoration_day.split("-")[0])
    commemoration_month = int(commemoration_day.split("-")[1])
    commemoration_day = int(commemoration_day.split("-")[2])
    commemoration_date = date(commemoration_year, commemoration_month, commemoration_day)
    # 获取纪念日的日期差
    commemoration_days = str(today.__sub__(commemoration_date)).split(" ")[0]
    return commemoration_days


def get_commemoration_data(today, config_data):
    # 获取所有纪念日数据
    commemoration_days = {}
    for k, v in config_data.items():
        if k[0:13] == "commemoration":
            commemoration_days[k] = get_commemoration_day(today, v)
    return commemoration_days


def get_countdown_data(today, config_data):
    # 获取所有倒计时数据
    countdown_data = {}
    for k, v in config_data.items():
        if k[0:9] == "countdown":
            countdown_year = int(v.split("-")[0])
            countdown_month = int(v.split("-")[1])
            countdown_day = int(v.split("-")[2])
            countdown_date = date(countdown_year, countdown_month, countdown_day)
            if today == countdown_date:
                countdown_data[k] = 0
            else:
                countdown_data[k] = str(countdown_date.__sub__(today)).split(" ")[0]
    return countdown_data


def get_date():
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    os.environ['TZ'] = 'Asia/Shanghai'
    tzset()
    # date1 = datetime.now()
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    today_week = "{} {}".format(today, week)
    return today, today_week, year


def get_weather(region, config_data, weather_type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    if weather_type == 2:
        try:
            key = config_data["tian_api"]
        except KeyError:
            data = "未配置天行数据key"
            return data, data, data, data, data, data, data, data, data, data
        region_url = "http://api.tianapi.com/citylookup/index?key={}&area={}".format(key, region)
        response = requests.get(region_url, headers=headers).json()
        if response["code"] == 200:
            ad_code = response["newslist"][0]["adcode"]
            # return ad_code, ad_code, ad_code, ad_code, ad_code, ad_code, ad_code, ad_code, ad_code, ad_code
            weather_url = "http://api.tianapi.com/tianqi/index?key={}&city={}&type=1".format(key, ad_code)
            response = requests.get(weather_url, headers=headers).json()
            # 天气
            weather = response["newslist"][0]["weather"]
            # 当前温度
            temp = response["newslist"][0]["real"]
            # 风向
            wind_dir = response["newslist"][0]["wind"]
            # 最高气温
            max_temp = response["newslist"][0]["highest"]
            # 最低气温
            min_temp = response["newslist"][0]["lowest"]
            # 日出时间
            sunrise = response["newslist"][0]["sunrise"]
            # 日落时间
            sunset = response["newslist"][0]["sunset"]
            # 空气质量
            category = response["newslist"][0]["quality"]
            # pm2.5
            pm2p5 = "天行数据暂未返回pm2.5数据"
            # 今日建议
            proposal = response["newslist"][0]["tips"]
            return weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal
        else:
            data = response["msg"]
            return data, data, data, data, data, data, data, data, data, data
    else:
        try:
            key = config_data["weather_key"]
        except KeyError:
            data = "未配置和风天气key"
            return data, data, data, data, data, data, data, data, data, data
        region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
        response = requests.get(region_url, headers=headers).json()
        if response["code"] == "404":
            # print("地区数据找不到")
            data = "地区数据找不到"
            return data, data, data, data, data, data, data, data, data, data
        elif response["code"] == "401":
            # print("未配置和风天气key或key配置错误")
            data = "未配置和风天气key或key配置错误"
            return data, data, data, data, data, data, data, data, data, data
        else:
            # 获取地区的location--id
            location_id = response["location"][0]["id"]
        weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
        response = requests.get(weather_url, headers=headers).json()
        # 天气
        weather = response["now"]["text"]
        # 当前温度
        temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
        # 风向
        wind_dir = response["now"]["windDir"]
        # 获取逐日天气预报
        url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
        response = requests.get(url, headers=headers).json()
        # 最高气温
        max_temp = response["daily"][0]["tempMax"] + u"\N{DEGREE SIGN}" + "C"
        # 最低气温
        min_temp = response["daily"][0]["tempMin"] + u"\N{DEGREE SIGN}" + "C"
        # 日出时间
        sunrise = response["daily"][0]["sunrise"]
        # 日落时间
        sunset = response["daily"][0]["sunset"]
        url = "https://devapi.qweather.com/v7/air/now?location={}&key={}".format(location_id, key)
        response = requests.get(url, headers=headers).json()
        if response["code"] == "200":
            # 空气质量
            category = response["now"]["category"]
            # pm2.5
            pm2p5 = response["now"]["pm2p5"]
        else:
            # 国外城市获取不到数据
            category = ""
            pm2p5 = ""
        id = random.randint(1, 16)
        url = "https://devapi.qweather.com/v7/indices/1d?location={}&key={}&type={}".format(location_id, key, id)
        response = requests.get(url, headers=headers).json()
        proposal = ""
        if response["code"] == "200":
            proposal += response["daily"][0]["text"]
        return weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 获取农历生日的生日
        try:
            year_date = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("请检查生日的日子是否在今年存在")
            sys.exit(1)

    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_birth_data(year, config_data, today):
    # 获取所有生日数据
    birthdays = {}
    for k, v in config_data.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    birthday_dict = {}
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        birthday_dict[key] = birthday_data
    return birthday_dict


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


def replace_txt(txt, today_week, commemoration_data, birthday_data, note_ch, note_en, horoscope_data, countdown_data,
                region_data, name, auther,picUrl,avatarUrl,content):
    txt = txt.replace("date", today_week)
    txt = txt.replace("note_ch", note_ch)
    txt = txt.replace("note_en", note_en)
    # 替换天行数据
    txt = txt.replace("name", name)
    txt = txt.replace("auther", auther)
    txt = txt.replace("picUrl", picUrl)
    txt = txt.replace("avatarUrl", avatarUrl)
    txt = txt.replace("content", content)
    # 替换地区数据
    for key, value in region_data.items():
        txt = txt.replace(key, value)
    # 替换生日数据
    for key, value in birthday_data.items():
        txt = txt.replace(key, value)
    # 替换纪念日数据
    for key, value in commemoration_data.items():
        txt = txt.replace(key, value)
    # 替换星座数据
    for key, value in horoscope_data.items():
        txt = txt.replace(key, value)
    # 替换倒计时数据
    for key, value in countdown_data.items():
        txt = txt.replace(key, value)
    return txt


def get_access_token(config_data):
    # 企业 corp_id
    corp_id = config_data["corp_id"]
    # secret
    secret = config_data["secret"]
    # access_token
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(corp_id, secret)
    r = requests.get(url).json()
    if r["errcode"] == 0:
        accessToken = r["access_token"]
    else:
        print("获取access_token失败，请检查corp_id和secret是否正确")
        sys.exit(1)
    return accessToken


def send_message(access_token, description, to_user, config_data):
    content = description.replace("\n", "\\n") if description else None
    try:
        link = config_data["link"]
        if link == "":
            link = "weixin.qq.com/download"
    except KeyError:
        link = "weixin.qq.com/download"
    send_message_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token)
    msgtype = config_data["msg_type"]
    data = {"touser": to_user, "agentid": config_data["agent_id"], "enable_id_trans": 0, "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800, "msgtype": msgtype}
    if msgtype == "textcard":
        data["textcard"] = {
            "title": config_data["title"],
            "description": description,
            "url": "{}?title={}&content={}".format(link, config_data["title"], content),
            "btntxt": "详情"
        }
    elif msgtype == "text":
        data["text"] = {"content": "{}\n{}".format(config_data["title"], description)}
    elif msgtype == "news":
        try:
            picurl = config_data["picurl"]
        except KeyError:
            picurl = ""
        if picurl == "":
            picurl = get_image_url()
        data["news"] = {
            "articles": [
                {
                    "title": config_data["title"],
                    "description": description,
                    "url": "{}?picurl={}&title={}&content={}".format(link, picurl, config_data["title"], content),
                    "picurl": picurl,
                }
            ]
        }
    r = requests.post(send_message_url, json=data).json()
    if r["errcode"] == 0:
        print("推送消息成功！")
    elif r["errcode"] == 60020:
        print("推送消息失败！ip未加入白名单")
        sys.exit(1)
    else:
        print("推送消息失败！")
        print(r)
        sys.exit(1)


def main():
    config_data = config.data
    # 获取accessToken
    accessToken = get_access_token(config_data)
    # 获取日期
    today, today_week, year = get_date()
    # 获取地区数据
    try:
        weather_type = config_data["weather_type"]
    except KeyError:
        weather_type = 1
    region_data = get_region_data(config_data, weather_type)
    # 获取纪念日数据
    commemoration_data = get_commemoration_data(today, config_data)
    # 获取倒计时数据
    countdown_data = get_countdown_data(today, config_data)
    # 获取每日金句数据
    try:
        note_ch = config_data["note_ch"]
        note_en = config_data["note_en"]
    except KeyError:
        note_ch, note_en = "", ""
    if note_ch == "" and note_en == "":
        # 获取词霸每日金句
        note_ch, note_en = get_ciba()
    # 获取生日数据
    birthday_data = get_birth_data(year, config_data, today)
    # 获取星座数据
    horoscope_data = get_horoscope(config_data)
    # 获取天行数据
    name, auther,picUrl,avatarUrl,content = get_tianhang(config_data)
    # 替换模板内容
    txt = template.txt
    description = replace_txt(txt, today_week, commemoration_data, birthday_data, note_ch, note_en, horoscope_data,
                              countdown_data, region_data, name, auther,picUrl,avatarUrl,content)
    try:
        to_user = config_data["to_user"]
        if to_user == "":
            to_user = "@all"
    except KeyError:
        to_user = "@all"
    # 发送消息
    send_message(accessToken, description, to_user, config_data)


def main_handler(event, context):
    url_data = event.get("queryString")
    if url_data:
        config_data = config.data
        # 获取accessToken
        accessToken = get_access_token(config_data)
        # 获取agentname
        agent_name = get_agent_name(config_data, accessToken)
        # 获取年份
        year = str(localtime().tm_year)
        html = handle_html(url_data, agent_name, year)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }
    else:
        main()
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": '{"code":"200","message":"企业微信消息发送成功"}'
        }
