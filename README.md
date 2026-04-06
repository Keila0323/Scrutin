# Scrutin — AI Job Scam Detector

Scrutin is an AI-powered job posting scam detector. Paste any job listing and Scrutin analyzes it for fraud signals — returning a scam risk score, red flags with severity levels, and a plain-English recommendation. Built because job scams are up 118% since 2022 and job seekers deserve protection.

## Live Deployments

| Version | URL | Description |
|---|---|---|
| **Portfolio** | [keila0323.github.io/Scrutin](https://keila0323.github.io/Scrutin) | Redesigned editorial frontend — split layout, instant load |
| **Full App** | [scrutin.onrender.com](https://scrutin.onrender.com) | Full-stack deployment with FastAPI backend |

## Features

- **Scam Risk Score** — 0–100 score indicating likelihood of fraud
- **Red Flag Detection** — 14+ fraud patterns flagged with severity levels (high / medium / low)
- **Legitimacy Signals** — positive indicators that suggest a real job posting
- **Plain-English Recommendation** — clear actionable advice on whether to proceed
- **Missing Info Alerts** — flags what a legitimate posting should have but doesn't

## Tech Stack

- **Backend:** Python, FastAPI
- **AI:** OpenAI GPT-4o
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Deployment:** Render (backend), GitHub Pages (frontend)
