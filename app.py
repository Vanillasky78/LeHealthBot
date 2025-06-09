import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

st.set_page_config(page_title="LeHealthBot", page_icon="🥗")
st.title("🥗 LeHealthBot")
st.markdown("Welcome to your personalized fat-loss meal recommender!")

# Initialize bot
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
bot = st.session_state.bot

# UI interaction
if bot.state == "INIT":
    st.write(bot.generate_response(""))

if bot.state == "ASKED_FATTY_HISTORY":
    fatty_history = st.radio("🩺 Have you ever been told you have fatty liver in a check-up?", ["yes", "no"])
    if st.button("Confirm"):
        st.write(bot.generate_response(fatty_history))
        st.rerun()

elif bot.state == "ASKED_GENDER":
    gender = st.radio("👤 Select your gender:", ["male", "female"])
    if st.button("Confirm gender"):
        st.write(bot.generate_response(gender))
        st.rerun()

elif bot.state == "ASKED_WEIGHT":
    weight = st.number_input("⚖️ Enter your current weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("Confirm current weight"):
        st.write(bot.generate_response(str(weight)))
        st.rerun()

elif bot.state == "ASKED_TARGET":
    target = st.number_input("🎯 Enter your target weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("Confirm target weight"):
        st.write(bot.generate_response(str(target)))
        st.rerun()

elif bot.state == "READY":
    if st.button("📋 Get today's meal recommendation"):
        st.markdown(bot.generate_response("next"))
