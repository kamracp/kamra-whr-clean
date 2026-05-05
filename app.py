import streamlit as st
import physics   # 🔥 stable import

st.set_page_config(page_title="WHR Auto Sizing Tool", layout="wide")

st.title("🔥 Waste Heat Recovery (WHR) Auto Sizing Tool")
st.markdown("### Minimal Input → Automatic Industrial Design")

# ---------------- INPUTS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    flow = st.number_input("Flue Gas Flow (Nm³/hr)", value=20000)

with col2:
    T_in = st.number_input("Gas IN Temp (°C)", value=250)

with col3:
    T_out = st.number_input("Gas OUT Temp (°C)", value=150)

# ---------------- RUN ----------------
if st.button("🚀 Run Auto Design"):

    result = physics.whr_sizing(flow, T_in, T_out)

    if result:

        st.success("✅ WHR Design Generated")

        colA, colB, colC = st.columns(3)

        colA.metric("Steam (TPH)", round(result["tph"],2))
        colB.metric("Velocity (m/s)", round(result["velocity"],2))
        colC.metric("ΔP (mmWC)", round(result["dp"],2))

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔥 Heat Recovery")
            st.write("Heat Available (kcal/hr):", round(result["Q"],0))

        with col2:
            st.subheader("📐 Area")
            st.write("Required:", round(result["A_required"],1))
            st.write("Actual:", round(result["A_actual"],1))

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("⚙️ Geometry")
            st.write("Tubes:", result["tubes"])
            st.write("Rows:", result["rows"])
            st.write("Diameter:", result["diameter"])
            st.write("Pitch:", round(result["pitch"],3))
            st.write("Length:", result["length"])

        with col4:
            st.subheader("💨 Flow Check")
            if result["velocity"] > 12:
                st.warning("High Velocity → erosion risk")

            if result["dp"] > 90:
                st.warning("High Pressure Drop")

            if result["A_actual"] < result["A_required"]:
                st.error("Insufficient Heat Transfer Area")
            else:
                st.success("Design OK")

    else:
        st.error("❌ No valid design found")