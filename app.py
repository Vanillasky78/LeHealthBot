import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

st.set_page_config(page_title="LeHealthBot", page_icon="🥗")
st.title("🥗 LeHealthBot")
st.markdown("Welcome to your personalized fat-loss meal recommender!")

# Initialize chatbot
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.response = ""
    st.session_state.progress = 0

bot = st.session_state.bot

# Display chatbot message
if st.session_state.response:
    st.markdown(st.session_state.response)

# Step 1: INIT → FATTY_HISTORY
if bot.state == "INIT":
    st.session_state.response = bot.generate_response("")
    st.rerun()

# Step 2: Ask about fatty liver
elif bot.state == "ASKED_FATTY_HISTORY":
    fatty_history = st.radio("🩺 Have you ever been told you have fatty liver in a medical check-up?", ["yes", "no"], key="fatty_history")
    if st.button("Confirm fatty liver history"):
        st.session_state.response = bot.generate_response(fatty_history)
        st.rerun()

# Step 3: Gender
elif bot.state == "ASKED_GENDER":
    gender = st.radio("👤 Select your gender:", ["male", "female"], key="gender")
    if st.button("Confirm gender"):
        st.session_state.response = bot.generate_response(gender)
        st.rerun()

# Step 4: Weight
elif bot.state == "ASKED_WEIGHT":
    weight = st.number_input("⚖️ Enter your current weight (kg):", min_value=30.0, max_value=200.0, key="weight")
    if st.button("Confirm current weight"):
        st.session_state.response = bot.generate_response(str(weight))
        st.rerun()

# Step 5: Target
elif bot.state == "ASKED_TARGET":
    target = st.number_input("🎯 Enter your target weight (kg):", min_value=30.0, max_value=200.0, key="target")
    if st.button("Confirm target weight"):
        st.session_state.response = bot.generate_response(str(target))
        st.rerun()

# Step 6: Ready → Recommend meals one by one
elif bot.state == "READY":
    max_recommendations = 3
    if st.session_state.progress < max_recommendations:
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
