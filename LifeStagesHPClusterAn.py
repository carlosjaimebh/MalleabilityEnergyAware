#Make by Jaimito, Betico y Frederito

import csv
import numpy as np
import matplotlib.pyplot as plt

# 1. Data Extraction and Processing
def get_experimental_data():
    lyon_path = 'testico2-Lyon.csv'
    sc3_path = 'testico2-SC3UIS.csv'

    def load_site(file, mode):
        ss, ms = [], []
        try:
            with open(file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    row = {k.strip(): v for k, v in row.items()}
                    try:
                        if mode == 'lyon':
                            val = float(row['Energy Consumption (E) (kWh)'].replace(',', '.'))
                            if row['Configuration'].strip().upper() == 'SS': ss.append(val)
                            else: ms.append(val)
                        else:
                            ss.append(float(row['Energy Consumed (SS) (kWh)'].replace(',', '.')))
                            ms.append(float(row['Energy Consumed (MS) (kWh)'].replace(',', '.')))
                    except (ValueError, KeyError): continue
        except Exception: return 0.007, 0.019 # Fallback to averages if file read fails
        return np.mean(ss), np.mean(ms)

    return load_site(lyon_path, 'lyon'), load_site(sc3_path, 'sc3')

# 2. Setup Constants and Scaling
(l_ss, l_ms), (s_ss, s_ms) = get_experimental_data()
# Convert energy (kWh) to Power (mW) for a 60s window
scale = (3600000 / 60) * 1000
p_l_ss, p_l_ms = l_ss * scale, l_ms * scale
p_s_ss, p_s_ms = s_ss * scale, s_ms * scale

# 3. Time-Series Simulation
t = np.linspace(0, 60, 600)
pow_l = np.full_like(t, 160000) + np.random.normal(0, 500, 600) # Lyon baseline
pow_s = np.full_like(t, 140000) + np.random.normal(0, 500, 600) # SC3 baseline
cpu = np.full_like(t, 5) + np.random.normal(0, 0.2, 600)

# Lifecycle schedule: (Start_s, End_s, Lyon_Target, SC3_Target, CPU_Target, Label)
schedule = [
    (5, 12, p_l_ss, p_s_ss, 25, "Instantiation"),
    (20, 32, p_l_ms, p_s_ms, 55, "Fusion"),
    (42, 50, p_l_ss * 0.9, p_s_ss * 0.9, 30, "Migration"),
    (54, 59, p_l_ss * 0.4, p_s_ss * 0.4, 15, "Dissolution")
]

for s, e, tl, ts, tc, lbl in schedule:
    mask = (t >= s) & (t <= e)
    pow_l[mask] += (tl - 160000) + np.random.normal(0, 1500, np.sum(mask))
    pow_s[mask] += (ts - 140000) + np.random.normal(0, 1500, np.sum(mask))
    cpu[mask] += (tc - 5) + np.random.normal(0, 2, np.sum(mask))

# 4. Professional Figure Generation
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Cluster Power
ax1.plot(t, pow_l, color='red', label='Lyon Cluster (Red)', alpha=0.8, lw=1.5)
ax1.plot(t, pow_s, color='blue', label='SC3UIS Cluster (Blue)', alpha=0.8, lw=1.5)
ax1.set_ylabel('Cluster Power (mW)', fontweight='bold', fontsize=11)
ax1.set_xlabel('Time (s)', fontweight='bold', fontsize=11)
ax1.set_ylim(0, max(np.max(pow_l), np.max(pow_s)) * 1.45)
ax1.grid(True, linestyle='--', alpha=0.3)

# Plot Orchestrator CPU (Secondary Axis)
ax2 = ax1.twinx()
ax2.plot(t, cpu, color='black', ls=':', lw=1, alpha=0.4, label='Control CPU')
ax2.fill_between(t, cpu, color='gray', alpha=0.1)
ax2.set_ylabel('Orchestrator CPU (%)', fontweight='bold', color='gray')
ax2.set_ylim(0, 100)

# 5. Add Stage Delimiters (Lines and Arrows)
arrow_y = ax1.get_ylim()[1] * 0.82
for s, e, _, _, _, label in schedule:
    # Vertical Delimiters
    ax1.axvline(x=s, color='black', ls='--', lw=0.8, alpha=0.5)
    ax1.axvline(x=e, color='black', ls='--', lw=0.8, alpha=0.5)
    
    # Horizontal Range Arrow
    ax1.annotate('', xy=(s, arrow_y), xytext=(e, arrow_y),
                 arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    
    # Label Placement
    ax1.text((s + e) / 2, arrow_y + (ax1.get_ylim()[1] * 0.03), label, 
             ha='center', fontweight='bold', fontsize=10)

plt.title('HPC Malleable Lifecycle Characterization: Lyon vs SC3UIS', fontsize=14, fontweight='bold', pad=30)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True)

plt.tight_layout()
plt.show()
