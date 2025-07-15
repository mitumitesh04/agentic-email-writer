#  Agentic Email Generator

An AI-powered Streamlit app that autonomously generates professional emails based on user-provided bullet points. It uses the `qwen2.5:0.5b` model via [Ollama](https://ollama.com) to analyze context, write emails, generate subject lines, and provide strategic insights.

##  Features

- **Full Autonomy**: AI decides the tone, urgency, and purpose.
- **Creative Variations**: Generates multiple tones like formal, friendly, and urgent.
- **Strategic Analysis**: Provides communication strategies and suggestions.
- **Subject Line Optimization**: Craft compelling and concise subject lines.
- **Improvement Suggestions**: AI reviews your email and suggests improvements.

---

##  Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Model: `qwen2.5:0.5b` (must be pulled via `ollama pull qwen2.5:0.5b`)

---

##  Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/agentic-email-generator.git
   cd agentic-email-generator
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Pull the model in Ollama (if not already):**
   ```bash
    ollama pull qwen2.5:0.5b
4. **Run the App:**
   ```bash
    streamlit run streamlit_app.py
Open in your browser at http://localhost:8501
---
## Author
**Built by Mitesh J Upadhya**
