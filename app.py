import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

st.set_page_config(page_title="LeHealthBot", page_icon="🥗")
st.markdown("<h1 style='font-size:48px;'>🥗 LeHealthBot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:gray;'>Your personalized fat-loss meal recommender</h3>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.response = ""
    st.session_state.progress = 0

bot = st.session_state.bot

# ✅ Only show chatbot response during meal recommendation stage
if bot.state == "READY" and st.session_state.response:
    st.markdown(st.session_state.response)

# 🩺 Step 1: Ask about fatty liver history
if bot.state == "INIT":
    st.session_state.response = bot.generate_response("")
    st.rerun()

elif bot.state == "ASKED_FATTY_HISTORY":
    st.subheader("🩺 Step 1: Fatty Liver History")
    fatty_history = st.radio(
        "Have you ever been told you have fatty liver in a medical check-up?",
        ["yes", "no"], key="fatty_history"
    )
    if st.button("✅ Confirm fatty liver history"):
        st.session_state.response = bot.generate_response(fatty_history)
        st.rerun()

# 👤 Step 2: Gender
elif bot.state == "ASKED_GENDER":
    st.subheader("👤 Step 2: Gender")
    gender = st.radio("Please select your gender:", ["male", "female"], key="gender")
    if st.button("✅ Confirm gender"):
        st.session_state.response = bot.generate_response(gender)
        st.rerun()

# ⚖️ Step 3: Weight
elif bot.state == "ASKED_WEIGHT":
    st.subheader("⚖️ Step 3: Current Weight")
    weight = st.number_input(
        "Please enter your current weight (kg):", min_value=30.0, max_value=200.0, key="weight"
    )
    if st.button("✅ Confirm current weight"):
        st.session_state.response = bot.generate_response(str(weight))
        st.rerun()

# 🎯 Step 4: Target Weight
elif bot.state == "ASKED_TARGET":
    st.subheader("🎯 Step 4: Target Weight")
    target = st.number_input(
        "Please enter your target weight (kg):", min_value=30.0, max_value=200.0, key="target"
    )
    if st.button("✅ Confirm target weight"):
        st.session_state.response = bot.generate_response(str(target))
        st.rerun()

# 🍽️ Step 5: Recommend Meals
elif bot.state == "READY":
    max_recommendations = 3
    st.subheader("🍽️ Step 5: Personalized Meal Recommendation")
    st.progress(st.session_state.progress / max_recommendations)

    if st.session_state.progress < max_recommendations:
        if st.button("📋 Get today's meal recommendation"):
            st.session_state.response = bot.generate_response("next")
            st.session_state.progress += 1
            st.rerun()
    else:
        st.success("✅ You've received all recommendations for today!")
        if st.button("🔄 Start Over"):
            for key in ["bot", "response", "progress"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
