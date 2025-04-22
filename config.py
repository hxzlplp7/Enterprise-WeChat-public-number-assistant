data = {
    # 企微配置
    # 企业ID
    "corp_id": "ww6ffad01a912133ee",
    # 企业应用Secret
    "secret": "iY25iDGGvcbMLlFx0XsR8fLgbqAebNT5nBx1-nreHzA",
    # 企微应用AgentId，AgentId不需要使用引号
    "agent_id": 1000002,
    # 接收者的账号，多个接收者请用|分隔，例如 "user1ID|user2ID"，不填则默认发送应用可见范围所有人
    "to_user": "",
    # 推送消息类型，图文可以携带图片发送，文字消息类型可显示的字数更多
    # 文本卡片 - textcard（普通文本卡片消息，消息长度512字节）
    # 文本 - text（普通文本消息，消息长度2048字节）
    # 图文 - news（图文消息，在普通文本卡片消息上的基础上，添加一张图片发送）
    "msg_type": "text",
    # 仅在msg_type为news生效，图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。如果为空则会发送随机图片
    "picurl": "",

    # 信息配置
    # 推送消息的标题
    "title": "网易云热评",
    # 天气接口选择，1为和风，2为天行，默认使用和风天气的接口
    "weather_type": 1,
    # 和风天气apikey，请注册和风天气账号获取，如不需要天气接口，可留空
    "weather_key": "f88da1e87643430ea88b7d50a5e2f289",
    # 天行数据apikey，请注册天行数据账号获取，如不需要天行接口，可留空
    "tian_api": "1b971898a6221722ebbb2f80a3aa3a92",
    # 所在地区
    # 选择和风天气接口，可为省，市，区，县，同时支持国外城市，例如伦敦
    # 选择天行数据接口，可为省，市，区，县，不支持国外城市，并且地区不能携带省、市、区、县，如广州市直接写广州即可
    "region": "六盘水",
    # 生日1，前面加r代表农历生日
    "birthday1": {"name": "小马", "birthday": "2002-11-11"},
    # 生日2
    "birthday2": {"name": "小林", "birthday": "r1997-01-01"},
    # 纪念日1，会计算累计时间，格式"YYYY-MM-DD"
    "commemoration_day1": "2021-10-11",
    # 纪念日2，同上
    "commemoration_day2": "2021-01-01",
    # 倒计时1，日期不小于当天日期
    "countdown1": "2022-12-31",
    # 倒计时2
    "countdown2": "2023-01-23",
    # 金句中文，如果为空，默认会读取金山的每日金句
    "note_ch": "",
    # 金句英文
    "note_en": "",
    # 星座运势1，12星座，aries 白羊座, taurus 金牛座, gemini 双子座, cancer 巨蟹座, leo 狮子座, virgo 处女座
    # libra 天秤座, scorpio 天蝎座, sagittarius 射手座, capricorn 摩羯座, aquarius 水瓶座, pisces 双鱼座
    "horoscope1": "scorpio",
    # 详情页链接
    "link": " ",
}
