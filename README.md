
# 企业微信公众号助手

## 项目简介

企业微信公众号助手是一个自动化工具，用于定期向企业微信用户推送个性化消息，包括天气预报、生日提醒、纪念日、倒计时、每日金句、星座运势等信息。此工具可用于企业内部信息推送、团队日常提醒等场景。

## 功能特点

- **天气信息推送**：支持多地区天气数据获取和推送
- **生日提醒**：支持阳历和农历生日提醒
- **纪念日计算**：自动计算纪念日天数并推送
- **倒计时功能**：为重要日期设置倒计时
- **每日金句**：推送每日励志金句
- **星座运势**：获取并推送星座运势信息
- **疫情数据**：获取地区疫情最新数据
- **热评数据**：获取网易云音乐热门评论
- **自定义模板**：支持自定义消息模板
- **多种消息类型**：支持文本卡片、纯文本、图文等消息类型

## 系统要求

- Python 3.6+
- 企业微信管理员权限
- 和风天气API或天行数据API账号（用于获取天气数据）

## 安装步骤

1. 克隆本仓库到本地或服务器：
```bash
git clone https://github.com/yourusername/Enterprise-WeChat-public-number-assistant.git
cd Enterprise-WeChat-public-number-assistant
```

2. 安装所需依赖：
```bash
pip install requests zhdate
```

3. 配置`config.py`文件（参考下方配置说明）

## 配置说明

在`config.py`文件中进行配置，主要包含以下内容：

```python
data = {
    # 企业微信配置
    "corp_id": "企业ID",
    "secret": "应用Secret",
    "agent_id": 应用ID,
    
    # 消息配置
    "title": "每日提醒",
    "msg_type": "textcard",  # 可选：textcard, text, news
    "to_user": "@all",  # 接收消息的用户，@all表示所有用户
    
    # API配置
    "weather_key": "和风天气API的key",
    "tian_api": "天行数据API的key",
    "weather_type": 1,  # 1表示使用和风天气，2表示使用天行数据
    
    # 地区配置
    "region1": "深圳",
    "region2": "北京",
    
    # 生日配置（支持阳历和农历）
    "birth1": {"name": "小明", "birthday": "2000-01-01"},  # 阳历生日
    "birth2": {"name": "小红", "birthday": "r2000-01-01"},  # 农历生日，前缀r表示农历
    
    # 纪念日配置
    "commemoration1": "2020-01-01",  # 示例：恋爱纪念日
    
    # 倒计时配置
    "countdown1": "2023-12-31",  # 示例：元旦倒计时
    
    # 星座配置
    "horoscope1": "白羊座",
    
    # 自定义金句
    "note_ch": "",  # 为空时自动获取词霸每日金句
    "note_en": "",
    
    # 详情页链接
    "link": "",  # 为空时使用默认链接
    
    # 图片链接(仅msg_type为news时有效)
    "picurl": ""  # 为空时使用必应每日一图
}
```

## 使用方法

### 本地运行

直接运行`index.py`文件：

```bash
python index.py
```

### 定时任务（Linux/macOS）

使用crontab设置定时任务：

```bash
# 编辑定时任务
crontab -e

# 添加以下内容（每天早上7:30推送）
30 7 * * * cd /path/to/Enterprise-WeChat-public-number-assistant && python index.py
```

### 云函数部署

本项目也支持部署到云函数（如腾讯云函数、阿里云函数计算等），以实现定时触发。请参考相应云服务提供商的文档进行部署。

## 模板配置

在`template.py`文件中可以自定义消息模板，使用特定的标记来替换相应的数据：

- `date`: 日期和星期
- `note_ch`/`note_en`: 每日金句（中/英）
- `region1`/`region2`等: 地区名称
- `weather1`/`weather2`等: 天气情况
- `temp1`/`temp2`等: 当前温度
- `max_temp1`/`min_temp1`等: 最高/最低温度
- `wind_dir1`/`wind_dir2`等: 风向
- `birth1`/`birth2`等: 生日提醒信息
- `commemoration1`等: 纪念日天数
- `countdown1`等: 倒计时天数
- `horoscope1`等: 星座运势

## 常见问题

1. **推送失败，提示"ip未加入白名单"**
   - 解决方案：在企业微信管理后台添加服务器IP到IP白名单

2. **无法获取天气数据**
   - 解决方案：检查和风天气API或天行数据API的key是否正确

3. **农历生日计算错误**
   - 解决方案：检查生日日期是否在当年存在（如农历闰月）

## 许可证

MIT License

## 贡献指南

欢迎提交Issues或Pull Requests来完善本项目。
