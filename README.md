<div align="center">

<img src="https://img.shields.io/badge/VALORANT-FF4655?style=for-the-badge&logo=valorant&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />

# ⚡ NeuralIQ
### AI-Powered Valorant Coaching Platform

*Analyze your gameplay. Identify your weaknesses. Climb the ladder.*

[Features](#-features) • [Screenshots](#-screenshots) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Roadmap](#-roadmap)

</div>

---

## 🎯 What is NeuralIQ?

NeuralIQ is a **full-stack AI coaching platform** for competitive Valorant players. It combines Machine Learning, Large Language Models, and Computer Vision to deliver personalized coaching insights — all running **100% locally** on your machine.

No subscription required to get started. No data sent to external AI services. Your gameplay data stays yours.

---

## ✨ Features

### 📊 Performance Dashboard
Real-time stats visualization with custom SVG charts — KDA evolution, agent winrates, map performance, and player profile radar.

### 🗺️ AI Heatmaps (K-Means Clustering)
Kill and death position clustering on official Valorant minimaps. Automatically identifies your danger zones and safe positions across 12 maps.

### 🤖 AI Coach — Mistral 7B
Chat with a local LLM that knows your match history, heatmap patterns, and economy stats. Ask anything, get coaching advice streamed in real time.

### 🔬 Per-Match Analysis
Select any match from your history and get a detailed breakdown — round by round kill patterns, early deaths, economy efficiency, first blood stats, and multi-kill moments.

### 🎬 Video Coach — LLaVA Vision AI
Upload an MP4 gameplay recording. NeuralIQ extracts key frames, analyzes your on-site positioning and minimap rotations using computer vision, then synthesizes a coaching report.

---

## 📸 Screenshots

### Overview — KPIs & Charts
![Overview](screenshots/overview.png)

### Match History
![Matches](screenshots/matches.png)

### K-Means Heatmaps
![Heatmaps](screenshots/heatmaps.png)

### Analysis Report
![Rapport](screenshots/rapport.png)

### AI Coach — Mistral 7B
![Coach IA](screenshots/coach.png)

### Per-Match Analysis
![Analyse Match](screenshots/analysis.png)

### Video Coach — LLaVA
![Coach Vidéo](screenshots/video_coach.png)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite, SVG/CSS Charts |
| **Backend** | Python 3.12, FastAPI, uvicorn |
| **AI — Clustering** | scikit-learn (K-Means), scipy (KDE) |
| **AI — LLM** | Mistral 7B via Ollama (local) |
| **AI — Vision** | LLaVA via Ollama, OpenCV |
| **Data** | Riot Games API, Henrik Dev API |
| **Auth** | Riot RSO OAuth2 (in progress) |

---

## ⚙️ Installation

### Prerequisites

- Ubuntu 20.04+ / WSL2 / Debian
- Python 3.10+
- Node.js 20+
- Git
- Nvidia GPU (recommended for Ollama)

### 1. Clone the repository

```bash
git clone https://github.com/Nxva83/NeuralIQ.git
cd NeuralIQ
```

### 2. Install Node.js 20

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20 && nvm use 20
```

### 3. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests pandas numpy scikit-learn matplotlib pillow scipy \
            fastapi uvicorn python-multipart httpx opencv-python-headless \
            python-jose[cryptography] passlib[bcrypt]
```

### 4. Install Ollama + AI models

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral   # 4.4 GB — text coaching
ollama pull llava     # 4.7 GB — video analysis
```

### 5. Install dashboard dependencies

```bash
cd dashboard
npm install
npm install recharts@2.12.7 --legacy-peer-deps
cd ..
```

---

## 🔑 API Keys

### Riot Games API Key
Get a free development key at [developer.riotgames.com](https://developer.riotgames.com) (refreshes every 24h).

```bash
export RIOT_API_KEY="RGAPI-xxxx-xxxx-xxxx-xxxx"
export HENRIK_API_KEY="HDEV-xxxx-xxxx-xxxx-xxxx"
```

> For permanent setup (fish shell):
> ```bash
> echo 'set -gx RIOT_API_KEY "RGAPI-..."' >> ~/.config/fish/config.fish
> echo 'set -gx HENRIK_API_KEY "HDEV-..."' >> ~/.config/fish/config.fish
> ```

---

## 🚀 Usage

### Step 1 — Fetch match data

```bash
source venv/bin/activate
python riot_pipeline.py --name "YourName" --tag "EUW" --matches 20
```

### Step 2 — Generate heatmaps

```bash
python heatmap.py --name "YourName" --tag "EUW"
```

### Step 3 — Launch the platform

```bash
# Terminal 1 — API
source venv/bin/activate
uvicorn api:app --reload --port 8000

# Terminal 2 — Dashboard
cd dashboard && npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Quick start (all in one)

```bash
chmod +x start.sh && ./start.sh
```

### Video analysis

```bash
python video_coach.py --video your_game.mp4 --frames 8
```

---

## 🗺️ Supported Maps

Ascent · Bind · Split · Haven · Fracture · Pearl · Icebox · Breeze · Lotus · Sunset · Abyss · Corrode

---

## 🔧 Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Riot API      │────▶│  riot_pipeline   │────▶│   data/*.json   │
│   Henrik API    │     │   (Python)       │     └────────┬────────┘
└─────────────────┘     └──────────────────┘              │
                                                           ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │   heatmap.py     │────▶│  output/*.png   │
                        │  K-Means + KDE   │     └────────┬────────┘
                        └──────────────────┘              │
                                                           ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  React Dashboard│◀────│    FastAPI       │◀────│  Ollama         │
│  Vite · :5173   │     │    :8000         │     │  Mistral + LLaVA│
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 📊 Roadmap

- [x] Match data pipeline (Riot + Henrik API)
- [x] K-Means heatmaps (12 maps)
- [x] FastAPI backend with streaming
- [x] React dashboard (7 pages)
- [x] LLM coaching — Mistral 7B
- [x] Per-match detailed analysis
- [x] Video coaching — LLaVA + OpenCV
- [ ] Riot RSO OAuth2 authentication
- [ ] Multi-user profiles (SQLite)
- [ ] Economy scoring module
- [ ] Docker deployment + VPS
- [ ] Mobile app (React Native)

---

## ❗ Troubleshooting

| Issue | Fix |
|-------|-----|
| Riot API key expired | Regenerate at developer.riotgames.com (24h TTL) |
| Port 8000 in use | `pkill -9 -f uvicorn` |
| npm peer deps error | `npm install --legacy-peer-deps` |
| Ollama not responding | `ollama serve` |
| Video analysis slow | Use `--frames 4` to reduce processing time |

---

## ⚖️ Legal

NeuralIQ is not endorsed by Riot Games and does not reflect their views.
VALORANT and all related assets are trademarks of Riot Games, Inc.
Match data is accessed via the official Riot Games API under their Terms of Service.

---

<div align="center">

**Built with ❤️ for the Valorant competitive community**

[⭐ Star this repo](https://github.com/Nxva83/NeuralIQ) · [🐛 Report a bug](https://github.com/Nxva83/NeuralIQ/issues) · [💡 Request a feature](https://github.com/Nxva83/NeuralIQ/issues)

</div>