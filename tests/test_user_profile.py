# tests/test_user_profile.py

from chatbot.user_profile import UserProfile

def test_calorie_recommendation_male():
    user = UserProfile(gender="male", current_weight=80, target_weight=70)
    kcal = user.recommend_calorie_intake()
    assert 1200 <= kcal <= 2000

def test_calorie_recommendation_female():
    user = UserProfile(gender="female", current_weight=65, target_weight=60)
    kcal = user.recommend_calorie_intake()
    assert 1200 <= kcal <= 2000
