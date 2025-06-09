import streamlit as st
from chatbot.personal_chatbot import FatLossChatBot

st.set_page_config(page_title="LeHealthBot", page_icon="🥗")
st.title("🥗 LeHealthBot")
st.write("Welcome to your personalized fat-loss meal recommender!")

if "bot" not in st.session_state:
    st.session_state.bot = FatLossChatBot()

bot = st.session_state.bot

if bot.state == "INIT":
    st.write(bot.generate_response(""))
    st.rerun()

elif bot.state == "ASKED_GENDER":
    gender = st.radio("Select your gender:", ["male", "female"])
    if st.button("Confirm gender"):
        st.write(bot.generate_response(gender))
        st.rerun()

elif bot.state == "ASKED_WEIGHT":
    weight = st.number_input("Enter your current weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("Confirm current weight"):
        st.write(bot.generate_response(str(weight)))
        st.rerun()

elif bot.state == "ASKED_TARGET":
    target = st.number_input("Enter your target weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("Confirm target weight"):
        st.write(bot.generate_response(str(target)))
        st.rerun()

elif bot.state == "READY":
    if st.button("📋 Get today's meal recommendations"):
        st.success("Here are your meal suggestions:")
        st.markdown(bot.generate_response(""))