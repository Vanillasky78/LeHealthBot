# LeHealthBot

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**LeHealthBot** is a personalized meal recommendation assistant designed to support individuals—especially those with or at risk of fatty liver disease—in managing daily calorie intake and avoiding high-risk foods like sugar and fried items.

It provides a friendly chatbot interface available in both CLI (terminal) and Streamlit UI (browser).

---

## Features

- **Personalized calorie intake calculation**  
  Based on gender, current weight, and target weight.

- **Conversational chatbot interaction**  
  Step-by-step health assistant available via command-line or Streamlit.

- **Fatty liver awareness screening**  
  Custom prompts to flag potential dietary risks.

- **Food filtering based on risk classification**  
  - High Risk: Sugar + Fried  
  - Moderate Risk: Sugar or Fried  
  - Low Risk: Healthy

- **Local food dataset** (500+ meals)  
  Curated and stored locally, no internet needed.

- **Streamlit version with progress control**  
  One-by-one meal suggestion flow with restart button and step markers.

---

## Project Structure

```
LeHealthBot/
├── chatbot/
│   ├── base.py               # Abstract chatbot base class
│   ├── personal_chatbot.py   # LeHealthBot logic + state
│   └── user_profile.py       # Calorie calculation logic
├── data/
│   └── food_plans_500_en.csv # 500+ meals data
├── tests/
│   └── test_user_profile.py  # Unit tests for calorie logic
├── config.py                 # Central config (keywords, thresholds)
├── app.py                    # Streamlit interface
├── run.py                    # Command-line chatbot interface
├── requirements.txt          # Python dependencies
└── README.md                 # You are here!
```

---

## Getting Started

### Requirements

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/Vanillasky78/LeHealthBot.git
cd LeHealthBot

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## How to Use

### CLI Mode (Terminal)

```bash
python run.py
```

You will be guided through:

- Fatty liver history screening  
- Gender selection  
- Current & target weight input  
- 3 personalized meal suggestions with calorie + risk level

---

### Streamlit Mode (Browser)

```bash
streamlit run app.py
```

Streamlit UI includes:

- Page-by-page guided interaction
- Confirm buttons for each step
- Progress bar and restart option
- Risk badges displayed with each meal

---

## Sample Flow

1. User answers: Yes to fatty liver history  
2. Selects gender: Male  
3. Inputs: Current: 85kg, Target: 75kg  
4. Receives 3 meal suggestions:
   - Calorie total  
   - Ingredients  
   - Instructions  
   - Risk badge: High / Moderate / Low

---

## Run Unit Tests

This project includes unit tests for calorie recommendation logic.

### To run tests:

```bash
# Activate environment
conda activate nlp

# Navigate to project root
cd ~/Documents/GitHub/LeHealthBot

# Run tests with proper import path
PYTHONPATH=. pytest
```

> Note: `PYTHONPATH=.` is required to correctly import modules like `from chatbot.user_profile import UserProfile`.

---

## Privacy & Ethics

- Runs 100% locally — no internet or cloud required  
- No personal data is stored or transmitted  
- Risk classification is rule-based and not a medical diagnosis  
- Open-source, non-commercial academic/research use only

---

## Upgrade Ideas

- [ ] Add BMI classification  
- [ ] User session memory across restarts  
- [ ] Export PDF meal plans  
- [ ] Multi-language support  
- [ ] Voice command input