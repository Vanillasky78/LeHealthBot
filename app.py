import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

st.set_page_config(page_title="LeHealthBot", page_icon="🥗")

# Header
st.title("🥗 LeHealthBot")
st.subheader("Your personalized fat-loss meal recommender")
st.markdown("---")

# Initialize session state
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.response = ""
    st.session_state.progress = 0

bot = st.session_state.bot

# Show last chatbot response (if any)
if st.session_state.response:
    st.markdown(st.session_state.response)

# === Step 1: INIT → Trigger bot start ===
if bot.state == "INIT":
    st.session_state.response = bot.generate_response("")
    st.rerun()

# === Step 2: Fatty Liver History ===
elif bot.state == "ASKED_FATTY_HISTORY":
    st.markdown("### 🩺 Step 1: Fatty Liver History")
    st.markdown("Have you ever been told you have **fatty liver** in a medical check-up?")
    fatty_history = st.radio("", ["yes", "no"], key="fatty_history")
    if st.button("✅ Confirm fatty liver history"):
        st.session_state.response = bot.generate_response(fatty_history)
        st.rerun()

# === Step 3: Gender ===
elif bot.state == "ASKED_GENDER":
    st.markdown("### 👤 Step 2: Gender")
    st.markdown("Please select your gender:")
    gender = st.radio("", ["male", "female"], key="gender")
    if st.button("✅ Confirm gender"):
        st.session_state.response = bot.generate_response(gender)
        st.rerun()

# === Step 4: Current Weight ===
elif bot.state == "ASKED_WEIGHT":
    st.markdown("### ⚖️ Step 3: Current Weight")
    st.markdown("Please enter your **current weight** (kg):")
    weight = st.number_input("", min_value=30.0, max_value=200.0, key="weight")
    if st.button("✅ Confirm current weight"):
        st.session_state.response = bot.generate_response(str(weight))
        st.rerun()

# === Step 5: Target Weight ===
elif bot.state == "ASKED_TARGET":
    st.markdown("### 🎯 Step 4: Target Weight")
    st.markdown("Please enter your **target weight** (kg):")
    target = st.number_input("", min_value=30.0, max_value=200.0, key="target")
    if st.button("✅ Confirm target weight"):
        st.session_state.response = bot.generate_response(str(target))
        st.rerun()

# === Step 6: Recommend Meals ===
elif bot.state == "READY":
    max_recommendations = 3

    st.markdown("### 🍽️ Today's Meal Recommendation")

    if st.session_state.progress < max_recommendations:
        st.markdown(f"**Progress:** {st.session_state.progress} / {max_recommendations}")
        if st.button("📋 Get recommendation"):
            st.session_state.response = bot.generate_response("next")
            st.session_state.progress += 1
            st.rerun()
    else:
        st.success("✅ You've seen all 3 recommendations for today!")
        if st.button("🔄 Start Over"):
            for key in ["bot", "response", "progress"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
