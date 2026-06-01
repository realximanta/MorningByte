# ☀️ MorningByte

A zero-cost, serverless daily briefing bot powered by GitHub Actions and Telegram.

Twice a day — **7:00 AM** and **8:00 PM** — MorningByte wakes up, collects data from three APIs, builds a clean message, sends it to your Telegram, and shuts down.

No VPS. No server. No database. No cost.

---

## 📦 What You Get

| Push | Time | Contents |
|------|------|----------|
| ☀️ Morning | 7:00 AM | Weather + Top 3 Headlines + Wikipedia Fact |
| 🌙 Evening | 8:00 PM | Top 3 Headlines + Wikipedia Fact |

---

## 🏗 Architecture

```
MorningByte/
├── .github/
│   └── workflows/
│       └── morningbyte.yml     ← GitHub Actions scheduler
├── src/
│   ├── weather.py              ← Open-Meteo (no key required)
│   ├── news.py                 ← NewsAPI top headlines
│   ├── wikipedia.py            ← Random Wikipedia fact
│   ├── telegram.py             ← Message builder + sender
│   └── main.py                 ← Glue: orchestrates everything
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Setup Guide

### Step 1 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token** (looks like `123456:ABC-DEF...`)

### Step 2 — Get Your Chat ID

1. Start a chat with your new bot (send `/start`)
2. Open Telegram and search for **@userinfobot**
3. Send `/start` — it will reply with your **Chat ID**

### Step 3 — Get a NewsAPI Key

1. Go to [https://newsapi.org](https://newsapi.org) and sign up (free)
2. Copy your **API Key**

### Step 4 — Fork & Configure the Repo

1. Fork this repository on GitHub
2. Go to **Settings → Secrets and variables → Actions**

Add these **Secrets**:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from Step 1 |
| `TELEGRAM_CHAT_ID` | Your chat ID from Step 2 |
| `NEWSAPI_KEY` | Your NewsAPI key from Step 3 |

Add these **Variables** (optional — these have defaults):

| Name | Example | Description |
|------|---------|-------------|
| `CITY_NAME` | `Nagaon` | Display name for weather |
| `CITY_LAT` | `26.3474` | Your city's latitude |
| `CITY_LON` | `92.6843` | Your city's longitude |
| `NEWS_COUNTRY` | `us` | NewsAPI country code |

> **Find your lat/lon:** [latlong.net](https://www.latlong.net)

### Step 5 — Enable Actions

1. Go to the **Actions** tab in your forked repo
2. Click **"I understand my workflows, go ahead and enable them"**

That's it. GitHub Actions will handle the rest.

---

## 🧪 Testing Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/MorningByte
cd MorningByte

# 2. Create your .env
cp .env.example .env
# Fill in your values in .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test morning push
MORNINGBYTE_PUSH=morning python src/main.py

# 5. Test evening push
MORNINGBYTE_PUSH=evening python src/main.py
```

---

## 📲 Example Outputs

**Morning:**
```
☀️ MorningByte

📅 02 June 2026

🌤 Nagaon
31°C • Partly Cloudy ⛅

📰 Headlines
1. Markets rally as Fed signals rate pause
2. New climate agreement signed at G7 summit
3. SpaceX launches 24 Starlink satellites

📚 Wikipedia
The Okapi
The okapi is a giraffid artiodactyl mammal native to the Congo. Despite resembling a zebra, it is the only living relative of the giraffe.

🚀 Time to build.
```

**Evening:**
```
🌙 EveningByte

📅 02 June 2026

📰 Headlines
1. Senate passes infrastructure amendment
2. Apple unveils new chip architecture
3. WHO issues update on tropical disease watch

📚 Wikipedia
Zoetrope
A zoetrope is a device that produces the illusion of motion from a rapid succession of static pictures.

✨ See you tomorrow.
```

---

## ⏰ Schedule

The workflow runs on UTC time. Default schedule is set for **IST (UTC+5:30)**:

| Push | IST | UTC Cron |
|------|-----|----------|
| Morning | 7:00 AM | `30 1 * * *` |
| Evening | 8:00 PM | `30 14 * * *` |

To change your timezone, adjust the cron times in `.github/workflows/morningbyte.yml`.
Use [crontab.guru](https://crontab.guru) to build your schedule.

---

## 🔧 Manual Trigger

Go to **Actions → MorningByte → Run workflow** and choose `morning` or `evening`.

---

## 📡 APIs Used

| API | Key Required | Docs |
|-----|-------------|------|
| [Open-Meteo](https://open-meteo.com) | ❌ Free, no key | Weather data |
| [NewsAPI](https://newsapi.org) | ✅ Free tier | Headlines |
| [Wikipedia REST](https://en.wikipedia.org/api/rest_v1/) | ❌ Free, no key | Random facts |
| [Telegram Bot API](https://core.telegram.org/bots/api) | ✅ Free | Message delivery |

---

## 🛠 Tech Stack

- **Python 3.12**
- **GitHub Actions** (scheduler + runner)
- **requests** (HTTP)
- **python-dotenv** (local env)

---

Built with ☕ — MorningByte v1
