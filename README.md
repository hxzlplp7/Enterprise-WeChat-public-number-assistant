# 🌟 Enterprise WeChat Official Account Assistant

[![GitHub License](https://img.shields.io/github/license/yourusername/Enterprise-weixin-public-number-assistant)](https://github.com/yourusername/Enterprise-weixin-public-number-assistant/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/Enterprise-weixin-public-number-assistant)](https://github.com/yourusername/Enterprise-weixin-public-number-assistant/stargazers)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/yourusername/Enterprise-weixin-public-number-assistant/main.yml)](https://github.com/yourusername/Enterprise-weixin-public-number-assistant/actions)

[English](README.md) | [简体中文](README_zh.md)

## 📖 Project Overview
The Enterprise WeChat Official Account Assistant is an automation tool designed to send personalized messages to WeChat enterprise users on a scheduled basis. It includes weather forecasts, birthday reminders, anniversaries, countdowns, daily quotes, horoscope predictions, and more.

## ✨ Features
- ☁️ **Weather Updates**: Supports fetching and pushing weather data for multiple regions
- 🎂 **Birthday Reminders**: Supports both Gregorian and Lunar calendar birthdays
- 🎉 **Anniversary Calculator**: Automatically calculates days since anniversaries and sends reminders
- ⏳ **Countdown**: Sets countdowns for important dates
- 💡 **Daily Quote**: Sends daily inspirational quotes
- ✨ **Horoscope**: Fetches and pushes horoscope information
- 🦠 **COVID-19 Statistics**: Retrieves the latest regional pandemic data
- 🎵 **Top Music Comments**: Fetches popular comments from NetEase Cloud Music
- 🛠️ **Custom Templates**: Supports custom message templates
- 📱 **Multiple Message Types**: Supports text cards, plain text, rich media, etc.

## ⚙️ System Requirements
- Python 3.6+
- WeChat Work administrator privileges
- HeWeather or TianAPI account (for weather data)

## 🚀 Installation Steps
1. Clone the repository locally or on your server:
   ```bash
   git clone https://github.com/yourusername/Enterprise-WeChat-public-number-assistant.git
   cd Enterprise-WeChat-public-number-assistant
   ```
2. Install dependencies:
   ```bash
   pip install requests zhdate
   ```
3. Configure `config.py` (see below for details)

## 🔧 Configuration Guide
Configure the following sections in `config.py`:

```python
data = {
    # WeChat Work credentials
    "corp_id": "Corp ID",
    "secret": "App Secret",
    "agent_id": Agent ID,
    
    # Message settings
    "title": "Daily Reminder",
    "msg_type": "textcard",  # Options: textcard, text, news
    "to_user": "@all",  # Recipient user(s), @all for everyone
    
    # API keys
    "weather_key": "HeWeather API key",
    "tian_api": "TianAPI key",
    "weather_type": 1,  # 1=HeWeather; 2=TianAPI
    
    # Regions
    "region1": "Shenzhen",
    "region2": "Beijing",
    
    # Birthdays (Gregorian & Lunar)
    "birth1": {"name": "Xiao Ming", "birthday": "2000-01-01"},
    "birth2": {"name": "Xiao Hong", "birthday": "r2000-01-01"},  # prefix r = Lunar calendar
    
    # Anniversaries
    "commemoration1": "2020-01-01",  # e.g., Relationship anniversary
    
    # Countdowns
    "countdown1": "2023-12-31",  # e.g., New Year countdown
    
    # Horoscope
    "horoscope1": "Aries",
    
    # Custom quotes
    "note_ch": "",  # If empty, fetch from CiBa daily quotes
    "note_en": "",
    
    # Detail page URL
    "link": "",
    
    # Image URL (only for msg_type=news)
    "picurl": ""
}
```

## 🏃‍♂️ Usage
### Run Locally
Run `index.py` directly:
```bash
python index.py
```

### Scheduled Tasks (Linux/macOS)
Use `crontab` to set up scheduled tasks:
```bash
# Edit crontab
crontab -e

# Add the following (daily at 07:30)
30 7 * * * cd /path/to/Enterprise-WeChat-public-number-assistant && python index.py
```

### Cloud Function Deployment
Supports Tencent Cloud Functions, Alibaba Cloud Functions, etc. Follow provider docs for setup.

## 📝 Template Customization
Customize `template.py` with these placeholders:

| Placeholder | Description |
| --------------------- | ------------------ |
| `date`                | Date & weekday |
| `note_ch` / `note_en` | Daily quote |
| `region1` / `region2` | Region names |
| `weather1` / `weather2` | Weather descriptions |
| `temp1` / `temp2`     | Current temperature |
| `max_temp1` / `min_temp1` | Max/Min temperature |
| `wind_dir1` / `wind_dir2` | Wind direction |
| `birth1` / `birth2`     | Birthday reminders |
| `commemoration1`        | Days since anniversary |
| `countdown1`            | Countdown days |
| `horoscope1`            | Horoscope |

## ❓ FAQ
1. **IP not whitelisted**
   - Solution: Add your server IP to the whitelist in the WeChat Work admin console
2. **Can't fetch weather data**
   - Solution: Verify your HeWeather or TianAPI key
3. **Lunar birthday calculation incorrect**
   - Solution: Ensure the date exists in the lunar calendar (e.g., leap months)

## 🙏 Sponsorship
This project is supported by the "Free VPS for Open Source Projects" program from VTEXS.
Thanks to VTEXS for supporting the open source community!

## 📜 License
MIT License

## 🤝 Contribution Guide
Contributions via Issues or PRs are welcome.

