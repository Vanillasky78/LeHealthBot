import streamlit as st
from chatbot.personal_chatbot import LeHealthBot

# ---------------- Header & Style ----------------
st.set_page_config(page_title="LeHealthBot", page_icon="🥗", layout="wide")

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3500/3500833.png", width=70)
with col2:
    st.markdown("""
        <h1 style='margin-bottom:0;'>LeHealthBot</h1>
        <h5 style='color:gray;'>Your personalized fat-loss meal recommender</h5>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- Initialize Bot ----------------
if "bot" not in st.session_state:
    st.session_state.bot = LeHealthBot()
    st.session_state.submitted = False
    st.session_state.progress = 0
bot = st.session_state.bot

# ---------------- Sidebar Progress ----------------
with st.sidebar:
    st.markdown("## 🧭 Progress")
    steps = [
        "Fatty Liver History",
        "Gender",
        "Current Weight",
        "Target Weight",
        "Meal Recommendation"
    ]
    state_map = {
        "ASKED_FATTY_HISTORY": 0,
        "ASKED_GENDER": 1,
        "ASKED_WEIGHT": 2,
        "ASKED_TARGET": 3,
        "READY": 4,
    }
    current_index = state_map.get(bot.state, -1)
    for i, step in enumerate(steps):
        icon = "✅" if i < current_index else "🔘" if i == current_index else "◻️"
        st.markdown(f"{icon} {step}")
    st.markdown("---")
    st.info("Click buttons only once per step.\nRefresh the page to start over.")

# ---------------- Main Interaction ----------------

if bot.state == "INIT":
    st.markdown("### 🩺 Step 1: Fatty Liver History")
    st.write(bot.generate_response(""))

elif bot.state == "ASKED_FATTY_HISTORY":
    st.markdown("### 🩺 Step 1: Fatty Liver History")
    st.write("Have you ever been told you have **fatty liver** in a medical check-up?")
    fatty_history = st.radio("Please select one:", ["yes", "no"])
    if st.button("✅ Confirm fatty liver history", disabled=st.session_state.submitted):
        st.write(bot.generate_response(fatty_history))
        st.session_state.submitted = True
        st.rerun()

elif bot.state == "ASKED_GENDER":
    st.markdown("### 👤 Step 2: Gender Selection")
    st.write(bot.generate_response(""))
    gender = st.radio("Select your gender:", ["male", "female"])
    if st.button("✅ Confirm gender", disabled=st.session_state.submitted):
        st.write(bot.generate_response(gender))
        st.session_state.submitted = True
        st.rerun()

elif bot.state == "ASKED_WEIGHT":
    st.markdown("### ⚖️ Step 3: Current Weight")
    st.write(bot.generate_response(""))
    weight = st.number_input("Enter your current weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("✅ Confirm current weight", disabled=st.session_state.submitted):
        st.write(bot.generate_response(str(weight)))
        st.session_state.submitted = True
        st.rerun()

elif bot.state == "ASKED_TARGET":
    st.markdown("### 🎯 Step 4: Target Weight")
    st.write(bot.generate_response(""))
    target = st.number_input("Enter your target weight (kg):", min_value=30.0, max_value=200.0)
    if st.button("✅ Confirm target weight", disabled=st.session_state.submitted):
        st.write(bot.generate_response(str(target)))
        st.session_state.submitted = True
        st.rerun()

elif bot.state == "READY":
    st.markdown("### 🍽️ Step 5: Personalized Meal Recommendation")
    if st.button("📋 Get today's meal recommendation"):
        recommendation = bot.generate_response("next")
        st.markdown(recommendation, unsafe_allow_html=True)
        if "That's all for today" in recommendation:
            st.success("🎉 You've seen all today's suggestions!")
        else:
            st.info("🔁 Click again for the next suggestion.")

# Reset flag to allow next click
st.session_state.submitted = False
