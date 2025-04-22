## 🌟 企业微信公众号助手 / Enterprise WeChat Official Account Assistant

### 📖 项目简介 / Project Overview
企业微信公众号助手是一个自动化工具，用于定期向企业微信用户推送个性化消息，包括天气预报、生日提醒、纪念日、倒计时、每日金句、星座运势等信息。

The Enterprise WeChat Official Account Assistant is an automation tool designed to send personalized messages to WeChat enterprise users on a scheduled basis. It includes weather forecasts, birthday reminders, anniversaries, countdowns, daily quotes, horoscope predictions, and more.

### ✨ 功能特点 / Features
- ☁️ **天气信息推送 / Weather Updates**：支持多地区天气数据获取和推送 / Supports fetching and pushing weather data for multiple regions
- 🎂 **生日提醒 / Birthday Reminders**：支持阳历和农历生日提醒 / Supports both Gregorian and Lunar calendar birthdays
- 🎉 **纪念日计算 / Anniversary Calculator**：自动计算纪念日天数并推送 / Automatically calculates days since anniversaries and sends reminders
- ⏳ **倒计时功能 / Countdown**：为重要日期设置倒计时 / Sets countdowns for important dates
- 💡 **每日金句 / Daily Quote**：推送每日励志金句 / Sends daily inspirational quotes
- ✨ **星座运势 / Horoscope**：获取并推送星座运势信息 / Fetches and pushes horoscope information
- 🦠 **疫情数据 / COVID-19 Statistics**：获取地区疫情最新数据 / Retrieves the latest regional pandemic data
- 🎵 **热评数据 / Top Music Comments**：获取网易云音乐热门评论 / Fetches popular comments from NetEase Cloud Music
- 🛠️ **自定义模板 / Custom Templates**：支持自定义消息模板 / Supports custom message templates
- 📱 **多种消息类型 / Multiple Message Types**：支持文本卡片、纯文本、图文等 / Supports text cards, plain text, rich media, etc.

### ⚙️ 系统要求 / System Requirements
- Python 3.6+
- 企业微信管理员权限 / WeChat Work administrator privileges
- 和风天气 API 或 天行数据 API 账号 / HeWeather or TianAPI account (for weather data)

### 🚀 安装步骤 / Installation Steps
1. 克隆本仓库到本地或服务器 / Clone the repository locally or on your server:
   ```bash
   git clone https://github.com/yourusername/Enterprise-WeChat-public-number-assistant.git
   cd Enterprise-WeChat-public-number-assistant
   ```
2. 安装所需依赖 / Install dependencies:
   ```bash
   pip install requests zhdate
   ```
3. 配置 `config.py` 文件 / Configure `config.py` (see below for details)

### 🔧 配置说明 / Configuration Guide
在 `config.py` 文件中进行配置，主要包含以下内容 / Configure the following sections in `config.py`:

```python
data = {
    # 企业微信配置 / WeChat Work credentials
    "corp_id": "企业ID / Corp ID",
    "secret": "应用 Secret / App Secret",
    "agent_id": 应用 ID / Agent ID,
    
    # 消息配置 / Message settings
    "title": "每日提醒 / Daily Reminder",
    "msg_type": "textcard",  # 可选：textcard, text, news / Options: textcard, text, news
    "to_user": "@all",  # 接收消息的用户 / Recipient user(s), @all for everyone
    
    # API 配置 / API keys
    "weather_key": "和风天气 API Key / HeWeather API key",
    "tian_api": "天行数据 API Key / TianAPI key",
    "weather_type": 1,  # 1=和风天气; 2=天行数据 / 1=HeWeather; 2=TianAPI
    
    # 地区配置 / Regions
    "region1": "深圳 / Shenzhen",
    "region2": "北京 / Beijing",
    
    # 生日配置 / Birthdays (Gregorian & Lunar)
    "birth1": {"name": "小明 / Xiao Ming", "birthday": "2000-01-01"},
    "birth2": {"name": "小红 / Xiao Hong", "birthday": "r2000-01-01"},  # 前缀 r 表示农历 / prefix r = Lunar calendar
    
    # 纪念日配置 / Anniversaries
    "commemoration1": "2020-01-01",  # 例：恋爱纪念日 / e.g., Relationship anniversary
    
    # 倒计时配置 / Countdowns
    "countdown1": "2023-12-31",  # 例：新年倒计时 / e.g., New Year countdown
    
    # 星座配置 / Horoscope
    "horoscope1": "白羊座 / Aries",
    
    # 自定义金句 / Custom quotes
    "note_ch": "",  # 为空时自动获取 / If empty, fetch from CiBa daily quotes
    "note_en": "",
    
    # 详情页链接 / Detail page URL
    "link": "",
    
    # 图片链接 / Image URL (仅 msg_type=news 有效)
    "picurl": ""
}
```

### 🏃‍♂️ 使用方法 / Usage
#### 本地运行 / Run Locally
直接运行 `index.py`:
```bash
python index.py
```

#### 定时任务 / Scheduled Tasks (Linux/macOS)
使用 `crontab` 设置定时任务:
```bash
# 编辑定时任务 / Edit crontab
crontab -e

# 添加以下内容（每天早上7:30推送） / Add the following (daily at 07:30)
30 7 * * * cd /path/to/Enterprise-WeChat-public-number-assistant && python index.py
```

#### 云函数部署 / Cloud Function Deployment
支持部署到腾讯云函数、阿里云函数等 / Supports Tencent Cloud Functions, Alibaba Cloud Functions, etc. Follow provider docs for setup.

### 📝 模板配置 / Template Customization
在 `template.py` 中自定义消息模板，使用以下占位符 / Customize `template.py` with these placeholders:

| 占位符 / Placeholder | 说明 / Description |
| --------------------- | ------------------ |
| `date`                | 日期和星期 / Date & weekday |
| `note_ch` / `note_en` | 每日金句 / Daily quote |
| `region1` / `region2` | 地区名称 / Region names |
| `weather1` / `weather2` | 天气情况 / Weather descriptions |
| `temp1` / `temp2`     | 当前温度 / Current temperature |
| `max_temp1` / `min_temp1` | 最高/最低温度 / Max/Min temperature |
| `wind_dir1` / `wind_dir2` | 风向 / Wind direction |
| `birth1` / `birth2`     | 生日提醒信息 / Birthday reminders |
| `commemoration1`        | 纪念日天数 / Days since anniversary |
| `countdown1`            | 倒计时天数 / Countdown days |
| `horoscope1`            | 星座运势 / Horoscope |

### ❓ 常见问题 / FAQ
1. **推送失败，提示 "ip 未加入白名单" / IP not whitelisted**
   - 解决：在企业微信管理后台添加服务器 IP 到白名单 / Add your server IP to the whitelist in the WeChat Work admin console
2. **无法获取天气数据 / Can't fetch weather data**
   - 解决：检查 API Key 是否正确 / Verify your HeWeather or TianAPI key
3. **农历生日计算错误 / Lunar birthday calculation incorrect**
   - 解决：检查日期是否存在闰月 / Ensure the date exists in the lunar calendar (e.g., leap months)

### 📜 许可证 / License
MIT License

### 🤝 贡献指南 / Contribution Guide
欢迎提交 Issues 或 Pull Requests 来完善本项目 / Contributions via Issues or PRs are welcome.

