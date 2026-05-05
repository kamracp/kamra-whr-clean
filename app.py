import streamlit as st
import physics   # ✅ IMPORTANT (module import)

st.set_page_config(page_title="WHR Auto Sizing Tool", layout="wide")

st.title("🔥 Waste Heat Recovery (WHR) Auto Sizing Tool")

# -------- INPUTS --------
flow = st.number_input("Flue Gas Flow (Nm³/hr)", value=20000)
T_in = st.number_input("Gas IN Temp (°C)", value=250)
T_out = st.number_input("Gas OUT Temp (°C)", value=150)

# -------- RUN --------
if st.button("🚀 Run Auto Design"):

    # ✅ FIX HERE
    result = physics.whr_sizing(flow, T_in, T_out)

    if result:

        st.success("✅ Design Generated")

        st.write("Steam (TPH):", round(result["tph"],2))
        st.write("Velocity:", round(result["velocity"],2))
        st.write("ΔP:", round(result["dp"],2))

        st.write("---")

        st.write("Tubes:", result["tubes"])
        st.write("Diameter:", result["diameter"])
        st.write("Pitch:", round(result["pitch"],3))
        st.write("Length:", result["length"])

    else:
        st.error("No valid design")