import streamlit as st
import os
from utils import *
from database import *

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Gig Insurance",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM CSS ----------------
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

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("📌 Navigation", ["Home", "Dashboard"])

# ---------------- LOGIN / REGISTER ----------------
if st.session_state.user is None:

    st.markdown("<div class='title'>🔐 AI Gig Insurance</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Secure your gig income with AI-powered insurance</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
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

# ---------------- MAIN APP ----------------
else:

    if menu == "Home":

        st.markdown("<div class='title'>🚀 AI Gig Insurance Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Real-time risk analysis & automatic payouts</div>", unsafe_allow_html=True)

        st.markdown("---")

        # -------- INPUT --------
        col1, col2, col3 = st.columns([2,2,1])

        location = col1.text_input("📍 City")
        income = col2.number_input("💰 Daily Income (₹)", min_value=100)

        if col3.button("🚀 Analyze"):

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
                    st.info(f"🌡 Temperature\n\n{temp} °C")

                with c2:
                    st.info(f"⛅ Weather\n\n{weather}")

                with c3:
                    st.info(f"🌫 AQI\n\n{aqi}")

                # -------- IMAGE ICON --------
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

                # -------- AI ANALYSIS --------
                st.subheader("📊 AI Analysis")

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("Risk Level", risk)

                with c2:
                    st.metric("Premium", f"₹{premium}")

                with c3:
                    st.metric("Workability Score", f"{score}/100")

                # -------- PAYOUT --------
                st.subheader("💸 Insurance Decision")

                if payout > 0:
                    st.success(f"₹{payout} payout triggered")
                    st.caption(reason)
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

    # ---------------- DASHBOARD ----------------
    elif menu == "Dashboard":

        st.subheader("📈 Earnings Dashboard")

        history = get_history(st.session_state.user)

        if history:
            st.line_chart(history)
        else:
            st.info("No history yet")

    # ---------------- LOGOUT ----------------
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
