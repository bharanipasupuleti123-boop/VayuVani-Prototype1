import streamlit as st
import pandas as pd
from data import DEMO_WEATHER_DATA
from engine import get_user_type_advice, answer_question

# --------------------------------------------------
# Page Setup
# --------------------------------------------------
st.set_page_config(
    page_title="VayuVani - Weather Information",
    page_icon="⛅",
    layout="wide"
)

# Custom Styling for clean, polished student weather app look
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1rem;
    }
    .demo-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar: Location, User Type & Demo Notice
# --------------------------------------------------
st.sidebar.markdown("## ⛅ VayuVani")
st.sidebar.caption("Weather Information")
st.sidebar.markdown("---")

locations = list(DEMO_WEATHER_DATA.keys())
selected_location = st.sidebar.selectbox(
    "Location",
    options=locations,
    index=0
)

user_types = ["General User", "Farmer", "Fisherman", "Disaster Response"]
selected_user_type = st.sidebar.selectbox(
    "User Type",
    options=user_types,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Demo weather data**  
    This application uses local demonstration weather data for evaluation and testing.
    """
)

# --------------------------------------------------
# Load Location Weather Data
# --------------------------------------------------
city_data = DEMO_WEATHER_DATA[selected_location]
current = city_data["current"]
forecast = city_data["forecast"]

# --------------------------------------------------
# Main Header
# --------------------------------------------------
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-header">⛅ VayuVani</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Weather Information</div>', unsafe_allow_html=True)
with col_badge:
    st.markdown(
        "<div style='text-align: right; padding-top: 10px;'><span class='demo-badge'>Demo weather data</span></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# --------------------------------------------------
# Today's Weather
# --------------------------------------------------
st.subheader(f"Today's Weather — {selected_location}")
st.caption(f"Observed condition: **{current['condition']}**")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Temperature", value=f"{current['temperature']} °C")
with m2:
    st.metric(label="Humidity", value=f"{current['humidity']} %")
with m3:
    st.metric(label="Wind", value=f"{current['wind_speed']} km/h")
with m4:
    st.metric(label="Rain Chance", value=f"{current['rain_probability']} %")

# Baseline Weather Advice for the selected user type
advice = get_user_type_advice(city_data, selected_user_type)
st.markdown(f"#### Weather Advice ({selected_user_type})")
if advice["type"] == "warning":
    st.warning(f"**{advice['title']}:** {advice['message']}")
elif advice["type"] == "success":
    st.success(f"**{advice['title']}:** {advice['message']}")
else:
    st.info(f"**{advice['title']}:** {advice['message']}")

st.markdown("---")

# --------------------------------------------------
# 3-Day Forecast
# --------------------------------------------------
st.subheader("3-Day Forecast")
col_cards, col_chart = st.columns([3, 2])

with col_cards:
    f_cols = st.columns(3)
    for i, day in enumerate(forecast):
        with f_cols[i]:
            with st.container(border=True):
                st.markdown(f"**{day['day_label']}**")
                st.caption(day["condition"])
                st.write(f"🌡️ **{day['temp_min']}°C – {day['temp_max']}°C**")
                st.write(f"🌧️ Rain Chance: **{day['rain_probability']}%**")
                st.write(f"💨 Wind: **{day['wind_speed']} km/h**")

with col_chart:
    st.markdown("**Rain Chance (%)**")
    chart_data = pd.DataFrame(
        {"Rain Chance (%)": [d["rain_probability"] for d in forecast]},
        index=[d["day_label"] for d in forecast]
    )
    st.bar_chart(chart_data, color="#3B82F6")

st.markdown("---")

# --------------------------------------------------
# Ask a Question & Get Answer
# --------------------------------------------------
st.subheader("Ask a Question")

# Initialize question in session state
if "current_question" not in st.session_state:
    st.session_state["current_question"] = ""
if "answer_result" not in st.session_state:
    st.session_state["answer_result"] = None

# Example Questions tailored to the selected user type
st.markdown("**Example Questions**")
example_dict = {
    "General User": [
        "Will it rain today?",
        "Do I need an umbrella?",
        "Is it warm outside?"
    ],
    "Farmer": [
        "Should I water my crops today?",
        "Is it safe to spray fertilizer?",
        "Will it rain tomorrow?"
    ],
    "Fisherman": [
        "Is it safe to go out to sea?",
        "How strong is the wind today?",
        "What are the sea conditions tomorrow?"
    ],
    "Disaster Response": [
        "Is there any flood risk?",
        "Are there high wind alerts?",
        "What is the severe weather outlook?"
    ]
}

current_examples = example_dict.get(selected_user_type, example_dict["General User"])
ex_cols = st.columns(len(current_examples))

for idx, eg_text in enumerate(current_examples):
    with ex_cols[idx]:
        if st.button(eg_text, key=f"eg_btn_{idx}", use_container_width=True):
            st.session_state["current_question"] = eg_text
            st.session_state["answer_result"] = answer_question(city_data, selected_user_type, eg_text)
            st.rerun()

# Text input for manual question entry
user_query = st.text_input(
    "Enter your question:",
    value=st.session_state.get("current_question", ""),
    placeholder="e.g. Will it rain tomorrow?",
    key="question_input"
)

if st.button("Get Answer", type="primary"):
    if user_query.strip():
        st.session_state["current_question"] = user_query.strip()
        st.session_state["answer_result"] = answer_question(city_data, selected_user_type, user_query.strip())
    else:
        st.warning("Please enter a question or select an example above.")

# Display Weather Advice / Answer
if st.session_state.get("answer_result"):
    ans = st.session_state["answer_result"]
    st.markdown("#### Weather Advice")
    with st.container(border=True):
        st.markdown(f"**Question:** {ans['question']}")
        if ans["status"] == "warning":
            st.warning(ans["answer"])
        elif ans["status"] == "success":
            st.success(ans["answer"])
        else:
            st.info(ans["answer"])

st.markdown("---")
st.caption("VayuVani • Demo weather data")