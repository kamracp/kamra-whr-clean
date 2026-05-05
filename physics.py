import math

# ---------------- HEAT ----------------
def heat_available(V, T1, T2):
    rho = 1.2 * (273/(T1+273))
    m = V * rho
    cp = 0.24
    Q = m * cp * (T1 - T2)
    return Q, m


# ---------------- STEAM ----------------
def steam_generation(Q, P, fw):
    return Q / 540000


# ---------------- OPTIMIZER ----------------
def geometry_optimizer(Q, m, T, T_sat, fw, P):

    best = None
    best_score = -1

    for d in [0.038, 0.05]:
        for L in [2.5, 3, 3.5]:
            for pitch_ratio in [1.3, 1.4, 1.5]:

                pitch = d * pitch_ratio
                free_area = pitch**2 - (math.pi * d**2 / 4)

                if free_area <= 0:
                    continue

                rho = 1.2 * (273/(T+273))
                m_sec = m / 3600

                # 🎯 Target velocity
                v_target = 10
                flow_area_target = m_sec / (rho * v_target)
                tubes = max(int(flow_area_target / free_area), 50)

                flow_area = tubes * free_area
                v = m_sec / (rho * flow_area)

                rows = max(int(math.sqrt(tubes)),1)
                dp = 1.5 * rows * (rho * v*v / 2) / 9.81

                # 🔥 Pinch / Approach scan
                for pinch in range(5, 15):
                    for approach in range(5, 12):

                        T_out = T_sat + pinch

                        Q_evap = m * 0.24 * (T - T_out)
                        Q_evap = max(Q_evap, 0)

                        tph = steam_generation(Q_evap, P, fw)

                        # ---------------- SCORE ENGINE ----------------
                        score = tph

                        # Velocity control
                        if v > 12:
                            score *= 0.6
                        elif v < 7:
                            score *= 0.7

                        # Pressure drop control
                        if dp > 100:
                            score *= 0.5
                        elif dp < 30:
                            score *= 0.8

                        # Pinch realism
                        if pinch <= 5:
                            score *= 0.6

                        # Approach realism
                        if approach < 6:
                            score *= 0.7

                        # Tube count penalty
                        if tubes > 400:
                            score *= 0.85

                        # Best selection
                        if score > best_score:
                            best_score = score
                            best = (d, pitch, L, tubes, v, dp, tph, pinch, approach, T_out)

    return best