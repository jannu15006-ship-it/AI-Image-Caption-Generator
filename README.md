<div align="center">

# 🖼️ AI Vision Image Caption Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Claude Vision](https://img.shields.io/badge/Claude_Vision-Anthropic-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

An intelligent Vision-Language web application that analyzes visual content and generates platform-optimized, tone-aware captions using Claude Vision.

</div>

---

## ✨ Features

- 📸 **Multi-Format Image Support:** Seamless handling of JPG, JPEG, PNG, and WEBP formats with real-time preview.
- 🎯 **Target Platform Customization:** Tailors output length, formatting, and hashtag style for **Instagram, Twitter / X, LinkedIn, YouTube, and General blogs**.
- 🎭 **Dynamic Tone Profiles:** Switch between **Funny, Emotional, Inspirational, Viral, Professional, and Poetic** personas.
- 🔐 **Secure Key Management:** In-app API key input with password masking, keeping credentials local and secure.
- 📋 **One-Click Clipboard Export:** Instant copy button to take generated captions directly to social platforms.
- 🛡️ **Robust Validation:** Graceful error handling for corrupted inputs, rate limits, and network anomalies.

---

## 🚀 Quickstart

### 1. Clone & Setup
```bash
git clone https://github.com/jannu15006-ship-it/AI-Image-Caption-Generator.git
cd AI-Image-Caption-Generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```

### 3. Usage
1. Enter your Anthropic Claude API key in the sidebar.
2. Upload any image file.
3. Select your target platform and desired tone.
4. Click **Generate Caption** and copy the synthesized result.

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit
- **Vision-Language Model:** Anthropic Claude Vision API
- **Language:** Python 3.8+

---

## 👩‍💻 Author
**Jahnavi Lalitha**
- GitHub: [@jannu15006-ship-it](https://github.com/jannu15006-ship-it)
