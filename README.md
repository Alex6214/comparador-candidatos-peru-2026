# 🇵🇪 Peru 2026 Candidate Comparator

An AI-powered web app that lets Peruvian citizens consult and compare presidential candidates for the **April 12, 2026 elections** using real-time web search.

🔗 **Live Demo:** [vota-informado-peru.streamlit.app](https://vota-informado-peru.streamlit.app)

---

## Features

- 🔍 **Candidate profiles** — biography, ideology, career background
- 📋 **Key proposals** per candidate fetched in real time
- ⚠️ **Scandals and legal alerts** from verified public sources
- ⚖️ **Side-by-side comparison** of two candidates on any topic
- 💬 **Free-form chat** — ask anything about any candidate
- 📱 **Fully responsive** — works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Groq — LLaMA 3.3 70B |
| Web Search | Tavily API |
| Language | Python 3.11 |
| Hosting | Streamlit Cloud |

---

## Project Structure
```
comparador-candidatos-peru-2026/
├── app.py                  # Main interface
├── config/
│   └── candidatos.py       # Official candidate list
├── services/
│   ├── ia_service.py       # Groq AI integration
│   └── search_service.py   # Tavily search integration
├── components/
│   └── perfil_card.py      # Candidate profile card
├── styles/
│   └── main.css            # Responsive styles
└── requirements.txt
```

---

## How It Works

1. User selects a candidate from the official JNE list
2. App searches the web in real time using Tavily
3. Groq LLaMA processes the information and generates a neutral profile
4. User can ask follow-up questions or compare two candidates

---

## Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/comparador-candidatos-peru-2026.git
cd comparador-candidatos-peru-2026
pip install -r requirements.txt
streamlit run app.py
```

Add your API keys to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-groq-key"
TAVILY_API_KEY = "your-tavily-key"
```

---

## Data Sources

- [JNE — Jurado Nacional de Elecciones](https://infogob.jne.gob.pe)
- [ONPE — Oficina Nacional de Procesos Electorales](https://www.onpe.gob.pe)
- Real-time news and public records via Tavily web search

---

## Disclaimer

This project is **educational and nonpartisan**. All information comes from public sources. Always verify with official sources before making electoral decisions.

---

Built by **Alexander Guevara** — Lima, Peru 🇵🇪