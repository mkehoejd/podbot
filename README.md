# The Walden Podcast (Marketing Robot) AKA PODBOT

**Walden Leadbot** is a self-updating outdoor and conservation lead generator built for automation, enrichment, and long-term audience growth — with no bloat and zero monthly SaaS fees.

Right now, it scrapes and enriches high-value contact leads from outdoor businesses, wildlife orgs, and conservation groups across the globe. Tomorrow, it'll do much more.

---

## 🏗️ Current Features

- 🔍 Randomized global search across outdoor and environmental sectors
- 🌐 Uses SerpAPI to gather business URLs from Google Search
- 🕵️‍♂️ Enriches those URLs with scraped emails and phone numbers
- 📈 Appends all cleaned leads into a master `.csv` file
- ⚙️ Auto-runs daily via `cron` or `launchd`
- 🧼 Skips duplicates and keeps all data organized in `/leads`

---

## 🚧 Roadmap

This bot is just getting started.

### 🔜 Next Features
- 📤 Push enriched leads to Google Sheets for easier team use
- 🧠 Plug ChatGPT in to auto-write custom email sequences
- ✉️ Integrate with free/cheap SMTP to drip cold emails
- 📊 Auto-track opens, clicks, and responses in Sheets
- 🗺️ Use feedback to refine lead types and prioritize high-conversion verticals

### 🪵 Long-Term Vision
- Fully autonomous, ethical cold-emailer that finds, writes to, and warms up new audiences for podcasts, products, and missions rooted in conservation, the outdoors, and intentional living.

---

## 🏃‍♂️ Quickstart

```bash
git clone https://github.com/mkehoejd/podbot.git
cd podbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
