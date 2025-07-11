# 🌧 QWeatherBot：基于和风天气的 Telegram 机器人

![Active users](https://weather.changchen.me/users/count)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/daya0576/he-weather-bot?link=https://github.com/daya0576/he-weather-bot/releases/)
![](https://img.shields.io/badge/Bot%20API-5.1-blue?logo=telegram)
![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m800876059-8ae4cb4cae57d1200261d8e6)

<img src="https://github.com/daya0576/he-weather-bot/blob/master/static/demo.gif?raw=true" width="600">

## ✨ Features

- [x] 支持发送定位或地名关键词设置所在地
- [x] 支持当日气温范围、晚间天气、天气灾害预警、次日天气播报
- [x] 支持自定义时间订阅天气，自动推送
- [x] 极端灾害天气预警（暴雨、台风等）
- [x] 钉钉机器人消息同步
- [ ] 多语言支持

## 👉 使用说明

无需部署开箱即用，戳链接调戏我：[t.me/he_weather_bot](https://t.me/he_weather_bot)

```shell
help - 帮助
weather - 获取实时天气（最近两天）
weather_6h - 获取实时天气（最近六小时）
set_location - 更新位置
set_api_key - 设置 API Key
subscribe - 开启订阅
unsubscribe - 关闭订阅
add_sub_locations - 新增子位置（支持多个）
delete_sub_locations - 移除子位置
```

## ⚡️ 自部署
docker compose 配置文件参考：
```shell
services:
  app:
    image: daya0576/he-weather-bot:latest
    environment:
      - ENV=production
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/he_weather_bot
      - TELEGRAM_BOT_WEBHOOK_ENDPOINT=<endpoint>/hook
      - TELEGRAM_BOT_API_KEY=<token>
    depends_on:
      - redis
      - db
    ports:
      - "18880:8080"
    networks:
      - app-network
  redis:
    image: redis:alpine
    # ports:
    #   - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network
  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
volumes:
  redis-data:
  postgres-data:
networks:
  app-network:
    driver: bridge
```

## 🚀 实现原理

[《如何零成本制作一个 telegram 机器人》](https://changchen.me/blog/20210221/buld-telegram-bot-from-scratch/)

## FAQ

Q. 有考虑支持多地区订阅吗(比如关心亲朋好友和出差人员)？  
支持 `add_sub_locations `命令添加子城市，`delete_sub_locations` 命令清除。

Q. 如何在群中播报？   
第一步：在群用户里添加机器人   
第二步：在群的输入框输入 / 符号，根据自动提示，点击输入 /help   
第三步：点击卡片的“定时订阅”修改推送的时间   
