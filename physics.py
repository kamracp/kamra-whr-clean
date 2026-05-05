import math

# ---------------- GAS PROPERTIES ----------------
def gas_props(T):
    rho = 1.2 * (273/(T+273))
    cp = 0.24
    return rho, cp

# ---------------- HEAT ----------------
def heat_available(V, T1, T2):
    rho, cp = gas_props(T1)
    m = V * rho
    Q = m * cp * (T1 - T2)
    return Q, m

# ---------------- STEAM ----------------
def steam_generation(Q, P, fw):
    return max(Q,0) / 540000

# ---------------- DEW POINT ----------------
def dew_point_water(H2O_pct):
    return 100 + 12 * math.log(max(H2O_pct,1))

def acid_dew_point(SO2_ppm):
    if SO2_ppm < 50:
        return 120
    return 120 + 0.04 * SO2_ppm

# ---------------- ZUKAUSKAS ----------------
def zukauskas_htc(v, d, rho, mu=2e-5, k=0.03, Pr=0.7):
    Re = rho * v * d / mu

    if Re < 100:
        C, m = 0.9, 0.4
    elif Re < 1000:
        C, m = 0.52, 0.5
    else:
        C, m = 0.27, 0.63

    Nu = C * (Re**m) * (Pr**0.36)
    h = Nu * k / d

    return h, Re

# ---------------- LMTD ----------------
def lmtd(dT1, dT2):
    if dT1 <= 0 or dT2 <= 0:
        return 1
    return (dT1 - dT2) / math.log(dT1/dT2)

# ---------------- FAN ----------------
def fan_selection(m, rho, dp, eff=0.7):
    flow = (m/3600)/rho
    power = flow * dp * 9.81 / (1000 * eff)

    if dp < 30:
        draft = "Natural Draft"
    elif dp < 150:
        draft = "Induced Draft"
    else:
        draft = "Forced Draft"

    return flow, power, draft

# ---------------- OPTIMIZER ----------------
def advanced_optimizer(V, T_in, fw_in, P, pinch, approach):

    Q, m = heat_available(V, T_in, T_in-100)

    T_sat = 100 + 5*P
    T_gas_out = T_sat + pinch
    T_fw_out = T_sat - approach

    best = None
    best_score = -1

    rho, cp = gas_props(T_in)
    m_sec = m/3600

    for d in [0.032, 0.038, 0.05]:
        for L in [2.5, 3, 3.5]:
            for pr in [1.3, 1.4, 1.5]:

                pitch = d * pr
                free_area = pitch**2 - (math.pi*d*d/4)

                if free_area <= 0:
                    continue

                v_target = 10
                area_req = m_sec / (rho * v_target)
                tubes = max(int(area_req / free_area), 40)

                flow_area = tubes * free_area
                v = m_sec / (rho * flow_area)

                rows = int(math.sqrt(tubes))
                dp = 1.3 * rows * (rho * v*v / 2) / 9.81

                h, Re = zukauskas_htc(v, d, rho)

                U = 1 / (1/h + 0.0005)

                LMTD = lmtd((T_in - T_fw_out), (T_gas_out - fw_in))

                A_required = Q / (U * LMTD)
                A_actual = tubes * math.pi * d * L

                tph = steam_generation(Q, P, fw_in)

                score = tph

                if v < 8 or v > 12:
                    score *= 0.7

                if dp > 90:
                    score *= 0.6

                if A_actual < A_required:
                    score *= 0.5

                if score > best_score:
                    best_score = score
                    best = {
                        "tph": tph,
                        "tubes": tubes,
                        "velocity": v,
                        "dp": dp,
                        "diameter": d,
                        "pitch": pitch,
                        "length": L,
                        "Re": Re,
                        "h": h,
                        "A_required": A_required,
                        "A_actual": A_actual,
                        "T_gas_out": T_gas_out,
                        "T_fw_out": T_fw_out,
                        "T_sat": T_sat,
                        "m": m,
                        "rho": rho
                    }

    return best