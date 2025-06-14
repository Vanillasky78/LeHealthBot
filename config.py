# config.py

SUGAR_KEYWORDS = ['sugar', 'honey', 'syrup']
FRIED_KEYWORDS = ['fried', 'deep-fried', 'battered']

MAX_DAILY_CALORIE = 2000

RISK_COLORS = {
    'high': "🔴 High Risk: Sugar + Fried",
    'moderate': "🟠 Moderate Risk: Sugar or Fried",
    'low': "🟢 Low Risk"
}

DEFAULT_CALORIES = {
    "base": 1800,
    "male_bonus": 200,
    "loss_penalty_per_kg": 20,
    "min": 1200
}
