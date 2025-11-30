# WetWell_Warrior.py
# Real Texas Wastewater Pump Control Simulation
# Built by a 23-year veteran operator — this is how it actually works.

import random
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

# Colored terminal output
init(autoreset=True)

# ==================== CONFIGURATION (Field Adjustable) ====================
SETPOINT_ON     = 25.0    # Pump turns ON when level drops to or below this
SETPOINT_OFF    = 45.0    # Pump turns OFF when level reaches or above this
MIN_OFF_TIME    = 60      # seconds — motor protection (anti-short cycling)

SIM_DURATION    = 1800    # seconds (30 minutes = perfect demo length)
TIME_STEP       = 10      # update every 10 seconds

INFLOW_RATE     = 0.75    # average incoming sewage flow (when pump off)
PUMP_RATE       = 0.85    # how fast the pump raises the level (when on)
SENSOR_NOISE    = 0.8     # because no sensor is perfect

# ==================== INITIAL STATE ====================
tank_level   = random.uniform(20, 50)
pump_on      = False
last_off_time = -9999

# Data logging
time_data    = []
level_data   = []
pump_data    = []   # for nice green bar on plot

print(Fore.MAGENTA + Style.BRIGHT + "WETWELL WARRIOR — Starting Real Plant Simulation\n")

# ==================== MAIN SIMULATION LOOP ====================
for t in range(0, SIM_DURATION + 1, TIME_STEP):
    # Add realistic sensor noise
    measured_level = tank_level + random.uniform(-SENSOR_NOISE, SENSOR_NOISE)

    # ——— PUMP CONTROL LOGIC (Exactly how you wired it) ———
    if (measured_level <= SETPOINT_ON 
        and not pump_on 
        and (t - last_off_time) >= MIN_OFF_TIME):
        pump_on = True
        print(Fore.GREEN + f"{t:4d}s → LEVEL LOW ({measured_level:.1f} ft) → PUMP ON")

    if measured_level >= SETPOINT_OFF and pump_on:
        pump_on = False
        last_off_time = t
        print(Fore.RED + f"{t:4d}s → LEVEL HIGH ({measured_level:.1f} ft) → PUMP OFF")

    # ——— PHYSICS (This is the magic that made yours work perfectly) ———
    if pump_on:
        tank_level += random.uniform(PUMP_RATE * 0.9, PUMP_RATE * 1.1)
    else:
        tank_level -= random.uniform(INFLOW_RATE * 0.8, INFLOW_RATE * 1.2)

    # Keep level in realistic bounds
    tank_level = max(0.0, min(50.0, tank_level))

    # ——— LOG DATA ———
    time_data.append(t)
    level_data.append(measured_level)
    pump_data.append(5 if pump_on else 0)  # height for green bar

    # Live status line
    status = Fore.CYAN + "PUMP ON " if pump_on else Fore.YELLOW + "pump off"
    print(f"{t:4d}s | Level: {measured_level:5.2f} ft | {status}")

# ==================== FINAL SCADA-STYLE PLOT ====================
plt.figure(figsize=(16, 9))
plt.plot(time_data, level_data, label="Wet Well Level (noisy sensor)", color="deepskyblue", linewidth=2.8)
plt.axhline(SETPOINT_ON,  color="green", linestyle="--", linewidth=2, label=f"Pump ON ≤ {SETPOINT_ON} ft")
plt.axhline(SETPOINT_OFF, color="red",   linestyle="--", linewidth=2, label=f"Pump OFF ≥ {SETPOINT_OFF} ft")
plt.fill_between(time_data, 0, pump_data, step="post", color="limegreen", alpha=0.7, label="Pump Running")

plt.title("WetWell Warrior — Real Texas Lift Station Control", fontsize=22, fontweight="bold", pad=20)
plt.xlabel("Time (seconds)", fontsize=14)
plt.ylabel("Tank Level (ft)", fontsize=14)
plt.legend(fontsize=12, loc="upper right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + "\nSimulation complete. .")
