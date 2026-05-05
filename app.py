import streamlit as st
from physics import *

st.title("🔥 WHR Boiler Engineering Tool")

flow = st.number_input("Gas Flow (Nm³/hr)", 20000)
T = st.number_input("Gas Temp (°C)", 250)
fw = st.number_input("Feed Water Temp (°C)", 30)
P = st.number_input("Pressure (bar)", 5)

if st.button("Run"):

    Q, m = heat_available(flow, T, T-100)

    tph = steam_generation(Q, P, fw)

    st.subheader("🔥 Steam")
    st.write("Steam:", round(tph,2), "TPH")

    T_sat = 100 + (P * 5)

    result = geometry_optimizer(Q, m, T, T_sat, fw, P)

    if result:
        d, pitch, L, tubes, v, dp, tph, pinch, approach, T_out = result

        st.subheader("⚙️ Geometry")
        st.write("Tubes:", tubes)
        st.write("Diameter:", d)
        st.write("Pitch:", round(pitch,3))

        st.subheader("💨 Flow")
        st.write("Velocity:", round(v,2))
        st.write("ΔP:", round(dp,2))

    else:
        st.error("❌ No valid design found")