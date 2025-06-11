import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

# ---------- Page Setup ----------
st.set_page_config(page_title="LeHealthBot", page_icon="🥗", layout="centered")

st.markdown("""
    <h1 style='font-size: 48px;'>🥗 LeHealthBot</h1>
    <h5 style='color: gray;'>Your personalized fat-loss meal recommender</h5>
    <hr style='margin-top:10px;margin-bottom:30px;'>
""", unsafe_allow_html=True)

# ---------- Initialize Session ----------
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.response = ""
    st.session_state.progress = 0

bot = st.session_state.bot

# ---------- Display Last Response ----------
if st.session_state.response:
    st.markdown(f"<div style='font-size:18px'>{st.session_state.response}</div>", unsafe_allow_html=True)

# ---------- Step 1: INIT ----------
if bot.state == "INIT":
    st.session_state.response = bot.generate_response("")
    st.rerun()

# ---------- Step 2: Fatty Liver History ----------
elif bot.state == "ASKED_FATTY_HISTORY":
    st.markdown("### 🩺 Step 1: Fatty Liver History")
    fatty_history = st.radio("Have you ever been told you have fatty liver in a medical check-up?",
                             ["yes", "no"], key="fatty_history")
    if st.button("✅ Confirm fatty liver history"):
        st.session_state.response = bot.generate_response(fatty_history)
        st.rerun()

# ---------- Step 3: Gender ----------
elif bot.state == "ASKED_GENDER":
    st.markdown("### 👤 Step 2: Gender")
    gender = st.radio("Please select your gender:", ["male", "female"], key="gender")
    if st.button("✅ Confirm gender"):
        st.session_state.response = bot.generate_response(gender)
        st.rerun()

# ---------- Step 4: Current Weight ----------
elif bot.state == "ASKED_WEIGHT":
    st.markdown("### ⚖️ Step 3: Current Weight")
    weight = st.number_input("Enter your current weight (kg):", min_value=30.0, max_value=200.0, key="weight")
    if st.button("✅ Confirm current weight"):
        st.session_state.response = bot.generate_response(str(weight))
        st.rerun()

# ---------- Step 5: Target Weight ----------
elif bot.state == "ASKED_TARGET":
    st.markdown("### 🎯 Step 4: Target Weight")
    target = st.number_input("Enter your target weight (kg):", min_value=30.0, max_value=200.0, key="target")
    if st.button("✅ Confirm target weight"):
        st.session_state.response = bot.generate_response(str(target))
        st.rerun()

# ---------- Step 6: Meal Recommendation ----------
elif bot.state == "READY":
    st.markdown("### 🍽️ Step 5: Personalized Meal Recommendation")

    max_recommendations = 3
    if st.session_state.progress < max_recommendations:
        st.progress((st.session_state.progress + 1) / max_recommendations)

        if st.button("📋 Get today's meal recommendation"):
            st.session_state.response = bot.generate_response("next")
            st.session_state.progress += 1
            st.rerun()
    else:
        st.success("✅ You've seen all recommendations for today!")

        if st.button("🔄 Start Over"):
            for key in ["bot", "response", "progress"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
