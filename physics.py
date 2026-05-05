import math

# ---------------- GAS PROPERTIES ----------------
def gas_props(T):
    rho = 1.2 * (273/(T+273))   # kg/m3
    cp = 0.24                   # kcal/kg-C
    return rho, cp


# ---------------- MAIN WHR SIZING ----------------
def whr_sizing(V, T_in, T_out):

    rho, cp = gas_props(T_in)

    m = V * rho                 # kg/hr
    m_sec = m / 3600            # kg/s

    Q = m * cp * (T_in - T_out) # kcal/hr
    tph = Q / 540000            # TPH approx

    best = None
    best_score = -1

    # ---------------- OPTIMIZATION ----------------
    for d in [0.032, 0.038, 0.05]:      # tube dia (m)
        for L in [2.5, 3.0, 3.5]:       # length (m)
            for pr in [1.3, 1.4, 1.5]:  # pitch ratio

                pitch = d * pr

                free_area = pitch**2 - (math.pi * d**2 / 4)

                if free_area <= 0:
                    continue

                # velocity design target
                v_target = 10

                flow_area_req = m_sec / (rho * v_target)
                tubes = max(int(flow_area_req / free_area), 50)

                flow_area = tubes * free_area
                velocity = m_sec / (rho * flow_area)

                rows = max(int(math.sqrt(tubes)), 1)

                dp = 1.3 * rows * (rho * velocity**2 / 2) / 9.81

                A_actual = tubes * math.pi * d * L

                # simple required area
                deltaT = max((T_in - T_out), 1)
                U = 35
                A_required = Q / (U * deltaT)

                # ---------------- SCORING ----------------
                score = tph

                if velocity < 8 or velocity > 11:
                    score *= 0.7

                if dp > 90:
                    score *= 0.6

                if A_actual < A_required:
                    score *= 0.5

                if tubes > 600:
                    score *= 0.8

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
                        "rows": rows
                    }

    return best