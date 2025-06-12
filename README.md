# 🥗 LeHealthBot

**LeHealthBot** is a personalized meal recommendation assistant designed to support individuals—especially those with or at risk of fatty liver disease—in managing daily calorie intake and reducing high-risk foods such as sugar and fried items.

It works through a friendly **chatbot interface** available in both **CLI** and **Streamlit UI** modes.

---

## ✨ Features

- 🔢 **Personalized calorie intake calculation**  
  Based on gender, current weight, and target weight.

- 💬 **Conversational interaction**  
  Step-by-step chatbot for both command-line and visual UI.

- 🩺 **Fatty liver awareness screening**  
  Custom prompts and dietary risk control.

- 🧠 **Food filtering based on risk classification**
  - 🔴 High Risk: Sugar + Fried
  - 🟠 Moderate Risk: Sugar or Fried
  - 🟢 Low Risk: Healthy

- 📂 **Local food dataset** (500+ meals)

- 🔄 **Streamlit version with progress control**  
  One-by-one suggestion flow with restart option.

---

## 📁 Project Structure

```
LeHealthBot/
├── chatbot/
│   ├── base.py               # Abstract chatbot base class
│   ├── personal_chatbot.py   # LeHealthBot chatbot logic
│   └── user_profile.py       # Calorie calculation engine
├── data/
│   └── food_plans_500_en.csv # 500+ food plans
├── app.py                    # Streamlit app (GUI)
├── run.py                    # CLI chatbot
├── requirements.txt          # Python dependencies
└── README.md                 # 📄 You're here!
```

---

## 🚀 Getting Started

### 🛠 Requirements

- Python 3.8+
- pip

### 📦 Installation

```bash
git clone https://github.com/Vanillasky78/LeHealthBot.git
cd LeHealthBot

# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Use

### CLI Version (Terminal)

```bash
python run.py
```

You’ll be guided to enter:

- Fatty liver history
- Gender
- Current + Target weight
- Receive 3 personalized food suggestions

---

### Streamlit UI Version (Browser)

```bash
streamlit run app.py
```

The web UI includes:

- 👣 Page-by-page chatbot flow
- ✅ Confirm buttons at each step
- 📊 Progress tracking + restart option
- 🟡 Risk icons for each suggestion

---

## ✅ Sample Flow

1. User chooses: Yes to fatty liver history  
2. Selects gender: Male  
3. Current: 85kg, Target: 75kg  
4. Recommender suggests 3 meals:
   - Each with calorie total, ingredients, instructions  
   - Shows colored risk badge: 🔴 / 🟠 / 🟢  

---

## 🔐 Privacy & Ethics

- LeHealthBot runs 100% locally  
- No personal data is stored or transmitted  
- Risk classification is rule-based (no medical diagnosis)  
- Open-source, non-commercial research use only  

---

## 📌 Upgrade Ideas

- ☐ Add BMI classification  
- ☐ User session memory  
- ☐ Export PDF meal plans  
- ☐ Multi-language support  
- ☐ Voice command integration  
