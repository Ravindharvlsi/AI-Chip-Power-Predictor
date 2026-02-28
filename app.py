import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("power_model.pkl")

st.title("AI-Based Chip Power Consumption Predictor")
st.write("Enter input parameters:")

# ---------------- INPUTS ----------------

sysbench_cpu = st.number_input("Sysbench CPU (%)", value=50.0)
frequency = st.number_input("Clock Frequency (GHz)", value=2.5)

voltage_1 = st.number_input("Voltage 1 (V)", value=220.0)
current_1 = st.number_input("Current 1 (A)", value=1.0)
power_factor_1 = st.number_input("Power Factor 1", value=0.9)

voltage_2 = st.number_input("Voltage 2 (V)", value=220.0)
current_2 = st.number_input("Current 2 (A)", value=1.0)
power_factor_2 = st.number_input("Power Factor 2", value=0.9)

# ---------------- CREATE INPUT DATA ----------------

input_data = pd.DataFrame([{
    "rpic": 0,
    "asmfish_1": 0,
    "asmfish_2": 0,
    "asmfish_3": 0,
    "asmfish_4": 0,
    "asmfish_5": 0,
    "sysbench_cpu": sysbench_cpu,
    "voltage_1": voltage_1,
    "power_factor_1": power_factor_1,
    "current_1": current_1,
    "voltage_2": voltage_2,
    "power_factor_2": power_factor_2,
    "current_2": current_2,
    "voltage_3": 0,
    "power_factor_3": 0,
    "current_3": 0,
    "voltage_4": 0,
    "power_factor_4": 0,
    "current_4": 0,
    "voltage_5": 0,
    "power_factor_5": 0,
    "current_5": 0,
    "voltage_6": 0,
    "power_factor_6": 0,
    "current_6": 0
}])

# ---------------- PREDICTION ----------------

if st.button("Predict Power"):

    # ML Prediction
    prediction = model.predict(input_data)
    ml_power = prediction[0]

    # Physics-based calculation
    physics_power_1 = voltage_1 * current_1 * power_factor_1
    physics_power_2 = voltage_2 * current_2 * power_factor_2
    physics_total = physics_power_1 + physics_power_2

    # Hybrid model (70% ML + 30% Physics)
    predicted_power = 0.7 * ml_power + 0.3 * physics_total

    # Display predicted power
    st.success(f"Predicted Total Power: {round(predicted_power, 2)} Watts")

    # ---------------- REAL-TIME GRAPH ----------------

    if "power_history" not in st.session_state:
        st.session_state.power_history = []

    st.session_state.power_history.append(predicted_power)

    if len(st.session_state.power_history) > 20:
        st.session_state.power_history.pop(0)

    st.markdown("### 📈 Real-Time Power Trend")
    st.line_chart(st.session_state.power_history)

    # ---------------- OPTIMIZATION ----------------

    st.markdown("### 🔧 AI-Based Power Optimization Suggestions")

    if predicted_power > 500:
        st.warning("High power consumption detected.")
        st.write("• Reduce supply voltage")
        st.write("• Enable DVFS (Dynamic Voltage and Frequency Scaling)")
        st.write("• Improve cooling system")

    elif predicted_power > 250:
        st.info("Moderate power usage.")
        st.write("• Monitor workload")
        st.write("• Check power factor efficiency")

    else:
        st.success("System operating efficiently.")

    # ---------------- SEMICONDUCTOR INSIGHT ----------------

    st.markdown("### 🧠 Semiconductor Insight")
    st.write("Dynamic power in CMOS circuits depends on V² and frequency scaling (DVFS).")