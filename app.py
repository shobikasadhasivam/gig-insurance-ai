import streamlit as st
import os
from utils import *
from database import *

st.set_page_config(page_title="Gig Insurance AI", layout="wide")

# -------- PREMIUM CSS --------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #dfe9f3, #ffffff);
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#2E7D32;
}

.subtitle {
    text-align:center;
    color:#555;
    margin-bottom:25px;
}

.glass {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    text-align:center;
}

.metric-card {
    padding: 15px;
    border-radius: 12px;
    background: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align:center;
}

button {
    border-radius: 10px !important;
    background-color: #4CAF50 !important;
    color: white !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -------- SESSION --------
if "user" not in st.session_state:
    st.session_state.user = None

# -------- LOGIN --------
if st.session_state.user is None:

    st.markdown("<div class='title'>🔐 Welcome</div>", unsafe_allow_html=True)

    option = st.radio("", ["Login", "Register"])

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if option == "Register":
        if st.button("Register"):
            register(user, pwd)
            st.success("Registered successfully!")

    else:
        if st.button("Login"):
            if login(user, pwd):
                st.session_state.user = user
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# -------- MAIN APP --------
else:

    st.markdown("<div class='title'>🚀 AI-Powered Insurance</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Protecting gig workers from income loss</div>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.user = None

    st.markdown("---")

    col1, col2 = st.columns(2)

    location = col1.text_input("📍 Enter your City")
    income = col2.number_input("💰 Daily Income (₹)", min_value=100)

    st.markdown("")

    if st.button("🚀 Analyze Now"):

        data = get_weather(location)

        if data.get("cod") != 200:
            st.error("Invalid city")
        else:
            temp = data["main"]["temp"]
            weather = data["weather"][0]["main"]
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            aqi = get_aqi(lat, lon)

            risk = calculate_risk(temp, weather, aqi)
            premium = calculate_premium(risk)
            payout, reason = calculate_payout(weather, temp, income, aqi)
            score = workability_score(weather, temp, aqi)

            # -------- LIVE CONDITIONS --------
            st.subheader("🌦 Live Conditions")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.image("images/temp.png", width=50)
                st.metric("Temperature", f"{temp}°C")
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.image("images/weather.png", width=50)
                st.metric("Weather", weather)
                st.markdown("</div>", unsafe_allow_html=True)

            with c3:
                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.image("images/aqi.png", width=50)
                st.metric("AQI", aqi)
                st.markdown("</div>", unsafe_allow_html=True)

            # -------- MAIN ICON --------
            icon = None
            if weather.lower() == "rain":
                icon = "images/rain.png"
            elif temp > 42:
                icon = "images/heat.png"
            elif aqi and aqi >= 4:
                icon = "images/pollution.png"

            if icon and os.path.exists(icon):
                col_img = st.columns([1,2,1])[1]
                with col_img:
                    st.image(icon, width=140)

            # -------- ANALYSIS --------
            st.subheader("📊 AI Analysis")

            c1, c2, c3 = st.columns(3)

            c1.markdown(f"<div class='metric-card'><h4>Risk</h4><h2>{risk}</h2></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h4>Premium</h4><h2>₹{premium}</h2></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><h4>Workability</h4><h2>{score}/100</h2></div>", unsafe_allow_html=True)

            # -------- PAYOUT --------
            st.subheader("💸 Insurance Decision")

            if payout > 0:
                st.success(f"₹{payout} Payout ({reason})")
                add_history(st.session_state.user, payout)
            else:
                st.info("No payout triggered")

            # -------- INSIGHT --------
            st.subheader("🧠 AI Insight")

            st.markdown("""
            <div class='glass'>
            This system uses real-time environmental data, AI risk scoring, and automated triggers to ensure gig workers are financially protected.
            </div>
            """, unsafe_allow_html=True)

    # -------- DASHBOARD --------
    st.markdown("---")
    st.subheader("📈 Earnings Dashboard")

    history = get_history(st.session_state.user)

    if history:
        st.line_chart(history)
    else:
        st.info("No history yet")