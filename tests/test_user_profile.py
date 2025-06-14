# tests/test_user_profile.py

import pytest
from chatbot.user_profile import UserProfile
from config import DEFAULT_CALORIES

@pytest.mark.parametrize(
    "gender, current, target, expected_range",
    [
        ("male", 80, 70, (DEFAULT_CALORIES["min"], DEFAULT_CALORIES["base"] + DEFAULT_CALORIES["male_bonus"])),
        ("female", 65, 60, (DEFAULT_CALORIES["min"], DEFAULT_CALORIES["base"])),
        ("female", 80, 80, (DEFAULT_CALORIES["min"], DEFAULT_CALORIES["base"])),
    ]
)
def test_calorie_recommendation(gender, current, target, expected_range):
    user = UserProfile(gender=gender, current_weight=current, target_weight=target)
    kcal = user.recommend_calorie_intake()
    assert expected_range[0] <= kcal <= expected_range[1], f"Calories {kcal} out of expected range {expected_range}"
