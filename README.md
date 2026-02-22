# 📰 RSS-Based Fake News Verification System

A **real-time fake news verification system** that works **without Machine Learning**.  
The system verifies news by comparing user input against live RSS feeds from trusted Indian news sources using rule-based text processing.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-2.3.3-red)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Verification Logic](#-verification-logic)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

This project aims to combat misinformation by providing an **evidence-based approach** to news verification.

Unlike ML-based solutions that operate as *black boxes*, this system maintains full transparency by showing users the exact matching articles and trusted sources used for verification.

### ✅ Why This Approach?

- 🔍 **No Black Box** — users see why news is flagged
- ⚡ **Real-time Verification** using live RSS feeds
- 📰 **Trusted Indian News Sources**
- 🪶 **Lightweight** — no ML models or training datasets required

---

## ✨ Features

### ✅ Core Functionality

- Real-time News Fetching from RSS feeds
- Rule-based Keyword Extraction (No ML)
- Similarity Scoring using text matching
- Verification Categories:

| Status | Meaning |
|------|------|
| ✅ Likely Real | Multiple trusted sources match |
| ⚠️ Partially Verified | Limited matches found |
| ❌ Possibly Fake / Unverified | No reliable matches |
| 🔍 Historical News | Old news detected |

---

### 💻 User Interface

- Clean responsive web interface
- Mobile-friendly layout
- Clickable evidence links
- Visual verification indicators
- Detailed verification metrics

---

### ⚙️ Technical Features

- Asynchronous RSS fetching
- Result caching
- Comprehensive logging
- Error handling & fallback mechanisms
- Auto-refresh capability

---

## 🔧 How It Works
User Input
↓
Keyword Extraction
↓
Fetch RSS Feeds
↓
Similarity Check
↓
Verification Result + Related News Links


### Workflow Explanation

#### 1️⃣ User Input Processing
- Remove special characters
- Stop-word removal
- Extract keywords & phrases
- Pattern detection

#### 2️⃣ News Fetching
- Parallel RSS feed fetching
- XML parsing (RSS & Atom)
- Duplicate removal
- Source tagging

#### 3️⃣ Similarity Calculation
- Exact keyword matching
- Partial word matching
- Phrase detection
- Category bonus scoring

#### 4️⃣ Verification Decision

| Score | Result |
|------|------|
| > 0.6 | Likely Real |
| > 0.4 | Partially Verified |
| < 0.4 | Possibly Fake |

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask 2.3.3**
- Flask-CORS
- Requests (RSS fetching)
- xml.etree.ElementTree (XML parsing)
- logging module
- Regular Expressions (`re`)

### Frontend
- HTML5
- CSS3 (Gradient UI)
- Vanilla JavaScript (ES6)
- Fetch API

---

## 📰 RSS News Sources

- The Hindu
- Indian Express
- Times of India
- NDTV
- Hindustan Times
- India Today

---

