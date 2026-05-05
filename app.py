import streamlit as st
from physics import *

st.title("🔥 WHR Advanced Engineering Tool")

# ---------------- INPUTS ----------------
flow = st.number_input("Gas Flow (Nm³/hr)", 20000)
T = st.number_input("Gas Temp (°C)", 250)
fw = st.number_input("Feed Water Temp (°C)", 30)
P = st.number_input("Pressure (bar)", 5)

pinch = st.slider("Pinch (°C)", 5, 25, 10)
approach = st.slider("Approach (°C)", 5, 25, 10)

H2O = st.slider("H2O %", 5, 20, 12)
SO2 = st.slider("SO2 ppm", 0, 500, 50)

# ---------------- RUN ----------------
if st.button("Run"):

    result = advanced_optimizer(flow, T, fw, P, pinch, approach)

    if result:

        dew_water = dew_point_water(H2O)
        dew_acid = acid_dew_point(SO2)
        dew_point = max(dew_water, dew_acid)

        flow_m3s, fan_kw, draft = fan_selection(
            result["m"], result["rho"], result["dp"]
        )

        st.subheader("🔥 Steam")
        st.write("TPH:", round(result["tph"],2))

        st.subheader("🌡 Thermal")
        st.write("Steam Temp:", result["T_sat"])
        st.write("Gas Out:", result["T_gas_out"])
        st.write("FW Out:", result["T_fw_out"])
        st.write("Dew Point:", round(dew_point,1))

        if result["T_gas_out"] < dew_point:
            st.error("⚠ Condensation Risk")

        st.subheader("⚙ Geometry")
        st.write("Tubes:", result["tubes"])
        st.write("Dia:", result["diameter"])
        st.write("Pitch:", round(result["pitch"],3))
        st.write("Length:", result["length"])

        st.subheader("💨 Flow")
        st.write("Velocity:", round(result["velocity"],2))
        st.write("ΔP:", round(result["dp"],2))

        st.subheader("🔥 Heat Transfer")
        st.write("Re:", int(result["Re"]))
        st.write("h:", round(result["h"],1))

        st.subheader("📐 Area")
        st.write("Required:", round(result["A_required"],1))
        st.write("Actual:", round(result["A_actual"],1))

        st.subheader("🌀 Fan")
        st.write("Flow:", round(flow_m3s,2))
        st.write("Power:", round(fan_kw,2))
        st.write("Draft:", draft)

        st.subheader("⚠ Design Check")

        if result["velocity"] > 12:
            st.warning("High velocity")

        if result["dp"] > 90:
            st.warning("High pressure drop")

        if result["A_actual"] < result["A_required"]:
            st.error("Insufficient heat transfer area")
        else:
            st.success("Design OK")

    else:
        st.error("No valid solution")