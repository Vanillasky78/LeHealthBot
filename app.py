import streamlit as st
from chatbot.personal_chatbot import LeHealthBot
import pandas as pd

# ✅ Optional: improve load speed with cache
@st.cache_data
def load_food_data(bot: LeHealthBot):
    return bot.food_df

# ✅ Set page config
st.set_page_config(page_title="LeHealthBot", page_icon="🥗")

# ✅ Title area
st.markdown("<h1 style='font-size:48px;'>🥗 LeHealthBot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:gray;'>Your personalized fat-loss meal recommender</h3>", unsafe_allow_html=True)
st.divider()

# ✅ Initialize session state
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.response = ""
    st.session_state.progress = 0

bot = st.session_state.bot

# ✅ Main logic branching
if bot.state == "INIT":
    st.session_state.response = bot.generate_response("")
    st.rerun()

elif bot.state == "ASKED_FATTY_HISTORY":
    st.markdown("### 🩺 Step 1: Fatty Liver History")
    fatty_history = st.radio(
        "Have you ever been told you have fatty liver in a medical check-up?",
        ["yes", "no"], key="fatty_history"
    )
    if st.button("✅ Confirm fatty liver history"):
        st.session_state.response = bot.generate_response(fatty_history)
        st.rerun()

elif bot.state == "ASKED_GENDER":
    st.markdown("### 👤 Step 2: Gender")
    gender = st.radio("Please select your gender:", ["male", "female"], key="gender")
    if st.button("✅ Confirm gender"):
        st.session_state.response = bot.generate_response(gender)
        st.rerun()

elif bot.state == "ASKED_WEIGHT":
    st.markdown("### ⚖️ Step 3: Current Weight")
    weight = st.number_input("Enter your current weight (kg):", min_value=30.0, max_value=200.0, key="weight")
    if st.button("✅ Confirm current weight"):
        st.session_state.response = bot.generate_response(str(weight))
        st.rerun()

elif bot.state == "ASKED_TARGET":
    st.markdown("### 🎯 Step 4: Target Weight")
    target = st.number_input("Enter your target weight (kg):", min_value=30.0, max_value=200.0, key="target")
    if st.button("✅ Confirm target weight"):
        st.session_state.response = bot.generate_response(str(target))
        st.rerun()

elif bot.state == "READY":
    st.markdown("### 🍽️ Step 5: Personalized Meal Recommendation")
    max_recommendations = 3
    st.progress(st.session_state.progress / max_recommendations)

    if st.session_state.response:
        st.markdown(st.session_state.response)

    if st.session_state.progress < max_recommendations:
        if st.button("📋 Get today's meal recommendation"):
            st.session_state.response = bot.generate_response("next")
            st.session_state.progress += 1
            st.rerun()
    else:
        st.success("✅ You've received all recommendations for today!")
        if st.button("🔄 Start Over"):
            for key in ["bot", "response", "progress"]:
                st.session_state.pop(key, None)
            st.rerun()
