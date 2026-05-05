import math

# -----------------------------
# GAS PROPERTIES
# -----------------------------
def gas_props(T):
    """
    Approx flue gas properties
    T in °C
    """
    rho = 1.2 * (273 / (T + 273))   # kg/m3
    cp = 0.24                       # kcal/kg-°C
    return rho, cp


# -----------------------------
# MAIN WHR SIZING ENGINE
# -----------------------------
def whr_sizing(V, T_in, T_out):
    """
    Inputs:
    V      = Flue gas flow (Nm3/hr)
    T_in   = Gas inlet temp (°C)
    T_out  = Gas outlet temp (°C)

    Output:
    Optimized WHR design dictionary
    """

    # -----------------------------
    # BASIC CALCULATIONS
    # -----------------------------
    rho, cp = gas_props(T_in)

    m = V * rho                    # kg/hr
    m_sec = m / 3600              # kg/s

    Q = m * cp * (T_in - T_out)   # kcal/hr

    # Steam generation (rough industrial thumb rule)
    tph = Q / 540000

    # -----------------------------
    # OPTIMIZATION START
    # -----------------------------
    best = None
    best_score = -1

    for d in [0.032, 0.038, 0.05]:       # tube diameter (m)
        for L in [2.5, 3.0, 3.5]:        # tube length (m)
            for pr in [1.3, 1.4, 1.5]:   # pitch ratio

                pitch = d * pr

                # free flow area per tube
                free_area = pitch**2 - (math.pi * d**2 / 4)

                if free_area <= 0:
                    continue

                # -----------------------------
                # TARGET VELOCITY DESIGN
                # -----------------------------
                v_target = 10  # m/s ideal

                flow_area_req = m_sec / (rho * v_target)

                tubes = max(int(flow_area_req / free_area), 50)

                flow_area = tubes * free_area

                velocity = m_sec / (rho * flow_area)

                # -----------------------------
                # PRESSURE DROP
                # -----------------------------
                rows = max(int(math.sqrt(tubes)), 1)

                dp = 1.3 * rows * (rho * velocity**2 / 2) / 9.81  # mmWC

                # -----------------------------
                # HEAT TRANSFER AREA
                # -----------------------------
                A_actual = tubes * math.pi * d * L

                # simple LMTD approximation
                deltaT = max(T_in - T_out, 1)

                U = 35  # kcal/m2-hr-°C (typical WHR range)

                A_required = Q / (U * deltaT)

                # -----------------------------
                # SCORING LOGIC
                # -----------------------------
                score = tph

                # velocity band control
                if velocity < 8 or velocity > 11:
                    score *= 0.7

                # pressure drop penalty
                if dp > 90:
                    score *= 0.6

                # under-designed area penalty
                if A_actual < A_required:
                    score *= 0.5

                # too large system penalty
                if tubes > 600:
                    score *= 0.8

                # -----------------------------
                # BEST DESIGN SELECTION
                # -----------------------------
                if score > best_score:
                    best_score = score
                    best = {
                        "tph": tph,
                        "Q": Q,
                        "tubes": tubes,
                        "velocity": velocity,
                        "dp": dp,
                        "diameter": d,
                        "pitch": pitch,
                        "length": L,
                        "A_required": A_required,
                        "A_actual": A_actual,
                        "rows": rows,
                        "mass_flow": m,
                        "density": rho
                    }

    return best