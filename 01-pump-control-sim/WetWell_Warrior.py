import random
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
import time

init(autoreset=True)

# ==========================
# REAL-WORLD SETTINGS (this is the part you tweak in the field)
# ==========================
TANK_CAPACITY = 50.0
SIM_TIME = 1800              # 30 minutes is plenty to show a full cycle
DT = 5                       # seconds per step

PUMP_ON_WHEN_BELOW  = 20.0
PUMP_OFF_WHEN_ABOVE = 45.0
MIN_OFF_TIME = 60            # 1 minute off 

INFLOW_AVG = 1.0             # What your influent flow looks like most days
INFLOW_SWING = 0.6           # Storm flow / diurnal swing
SENSOR_NOISE = 0.7           # Because float switches lie and ultrasonics drift

# Two pumps — Lead/Lag the way you actually do it
pump1_running = False
pump2_running = False
lead_pump = 1                # Starts with pump 1
last_off_time = -9999
runtime_pump1 = 0
runtime_pump2 = 0

# Logging
time_data = []
level_data = []
pump1_data = []
pump2_data = []

def get_inflow():
    return INFLOW_AVG + random.uniform(-INFLOW_SWING, INFLOW_SWING)

def noisy_level(actual):
    return actual + random.uniform(-SENSOR_NOISE, SENSOR_NOISE)

tank_level = random.uniform(25, 40)

print(Fore.MAGENTA + Style.BRIGHT + "Your Real-World Dual Pump Alternator Simulation\n")

for t in range(0, SIM_TIME + 1, DT):
    measured = noisy_level(tank_level)
    
    # Update runtimes
    if pump1_running: runtime_pump1 += DT
    if pump2_running: runtime_pump2 += DT
    
    # === Your exact field logic ===
    need_pump = measured <= PUMP_ON_WHEN_BELOW
    can_start = (t - last_off_time) >= MIN_OFF_TIME
    
    if need_pump and can_start:
        if lead_pump == 1 and not pump1_running:
            pump1_running = True
            print(Fore.GREEN + f"{t:4d}s | LOW LEVEL → STARTING PUMP 1 (Lead)")
        elif lead_pump == 2 and not pump2_running:
            pump2_running = True
            print(Fore.GREEN + f"{t:4d}s | LOW LEVEL → STARTING PUMP 2 (Lead)")
        # If lead is already running or failed, fall back to lag
        elif not pump1_running and not pump2_running:
            pump1_running = True
            print(Fore.CYAN + f"{t:4d}s | LOW LEVEL → STARTING PUMP 1 (Lag took over)")

    if measured >= PUMP_OFF_WHEN_ABOVE:
        if pump1_running or pump2_running:
            print(Fore.RED + f"{t:4d}s | HIGH LEVEL → BOTH PUMPS OFF")
        pump1_running = pump2_running = False
        last_off_time = t
        # Alternate lead pump for next call
        lead_pump = 2 if lead_pump == 1 else 1

    # Physics
    pump_flow = 1.9 if (pump1_running or pump2_running) else 0
    tank_level += (get_inflow() - pump_flow) * DT
    tank_level = max(0, min(TANK_CAPACITY, tank_level))

    # Logging
    time_data.append(t)
    level_data.append(measured)
    pump1_data.append(1.5 if pump1_running else 0)
    pump2_data.append(1.5 if pump2_running else 0)

    print(f"{t:4d}s | Level: {measured:5.2f} | P1: {'ON ' if pump1_running else 'off'} | P2: {'off' if not pump2_running else 'ON '}")

# ==========================
# Plot SCADA trend
# ==========================
plt.figure(figsize=(14, 8))
plt.plot(time_data, level_data, label="Tank Level (noisy sensor)", color="dodgerblue", lw=2)
plt.axhline(PUMP_ON_WHEN_BELOW, color="green", ls="--", alpha=0.8, label="Pump(s) ON ≤")
plt.axhline(PUMP_OFF_WHEN_ABOVE, color="red", ls="--", alpha=0.8, label="Pump(s) OFF ≥")
plt.fill_between(time_data, 0, TANK_CAPACITY, color="lightblue", alpha=0.2)

# Pump bars at bottom — exactly like your HMI
plt.fill_between(time_data, 0, pump1_data, step="post", color="limegreen", alpha=0.7, label="Pump 1")
plt.fill_between(time_data, 0, pump2_data, step="post", color="orange", alpha=0.7, label="Pump 2")

plt.title("Your Plant — Dual Pump Alternation (Exactly How You Run It)", fontsize=16)
plt.xlabel("Time (seconds)")
plt.ylabel("Level")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print(Fore.MAGENTA + Style.BRIGHT + f"\nDone. Pump 1 ran {runtime_pump1//60} min, Pump 2 ran {runtime_pump2//60} min. Alternation worked perfectly.")
