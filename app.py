import streamlit as st
from physics import *

result = advanced_optimizer(flow, T_in, fw, P, pinch, approach)

st.title("🔥 WHR Auto Sizing Tool")

# -------- ONLY 3 INPUTS --------
flow = st.number_input("Flue Gas Flow (Nm³/hr)", 20000)
T_in = st.number_input("Gas IN Temp (°C)", 250)
T_out = st.number_input("Gas OUT Temp (°C)", 150)

# -------- RUN --------
if st.button("Run Auto Design"):

    result = whr_sizing(flow, T_in, T_out)

    if result:

        st.subheader("🔥 Heat Recovery")
        st.write("Heat Available (kcal/hr):", round(result["Q"],0))

        st.subheader("🔥 Steam Generation")
        st.write("Steam (TPH):", round(result["tph"],2))

        st.subheader("⚙️ Geometry")
        st.write("Tubes:", result["tubes"])
        st.write("Diameter:", result["diameter"])
        st.write("Pitch:", round(result["pitch"],3))
        st.write("Length:", result["length"])

        st.subheader("💨 Flow")
        st.write("Velocity:", round(result["velocity"],2))
        st.write("ΔP:", round(result["dp"],2))

        st.subheader("📐 Area")
        st.write("Required:", round(result["A_required"],1))
        st.write("Actual:", round(result["A_actual"],1))

        st.subheader("⚠️ Design Check")

        if result["velocity"] > 12:
            st.warning("High velocity")

        if result["dp"] > 90:
            st.warning("High pressure drop")

        if result["A_actual"] < result["A_required"]:
            st.error("Insufficient heat transfer area")
        else:
            st.success("Design OK")

    else:
        st.error("No valid design found")