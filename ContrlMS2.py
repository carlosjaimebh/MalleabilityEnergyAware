#Code make by Jaimito, Betico y Frederito

import csv
import random
import matplotlib.pyplot as plt

def generate_continuum_data(duration_sec=60, samples_per_sec=10):
    """
    Generates synthetic data for a malleable control plane.
    Simulates: Instantiation, Fusion, Migration, and Dissolution.
    """
    data = []
    total_samples = duration_sec * samples_per_sec
    
    for i in range(total_samples):
        time = i / samples_per_sec
        
        # Baseline: Idle state (2000mW system power, 2% Orchestrator CPU) 
        power = 2000 + random.uniform(-30, 30)
        cpu = 2 + random.uniform(-0.3, 0.3)
        
        # Add Spikes for Lifecycle Phases [cite: 73]
        # Instantiation (5-10s): Rapid compute aggregate creation
        if 5 <= time <= 10:
            power += 800 + random.uniform(-50, 50)
            cpu += 12 + random.uniform(-1, 1)
        
        # Fusion (20-26s): Scaling by merging resources 
        elif 20 <= time <= 26:
            power += 1500 + random.uniform(-100, 100)
            cpu += 25 + random.uniform(-2, 2)
            
        # Migration (40-44s): Transferring execution context 
        elif 40 <= time <= 44:
            power += 700 + random.uniform(-40, 40)
            cpu += 10 + random.uniform(-1, 1)
            
        # Dissolution (54-58s): Dismantling and entering deep sleep 
        elif 54 <= time <= 58:
            power += 400 + random.uniform(-20, 20)
            cpu += 6 + random.uniform(-0.5, 0.5)
            
        data.append({'Seconds': time, 'Power_mW': power, 'CPU_Percent': cpu})
    
    return data

# 1. Generate and Save Data (The Digital Artifact)
dataset = generate_continuum_data()
with open('malleable_control_overhead.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Seconds', 'Power_mW', 'CPU_Percent'])
    writer.writeheader()
    writer.writerows(dataset)

# 2. Extract data for plotting
times = [row['Seconds'] for row in dataset]
powers = [row['Power_mW'] for row in dataset]
cpus = [row['CPU_Percent'] for row in dataset]

# 3. Create Visualization of Control Cost 
fig, ax1 = plt.subplots(figsize=(12, 6))

# System Power (Left Axis) 
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Total System Power (mW)', color='tab:red', fontsize=12)
ax1.plot(times, powers, color='tab:red', label='Total Power')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, linestyle='--', alpha=0.6)

# Control CPU Overhead (Right Axis - "Control Cost") 
ax2 = ax1.twinx()
ax2.set_ylabel('Orchestrator CPU Overhead (%)', color='tab:blue', fontsize=12)
ax2.fill_between(times, cpus, color='tab:blue', alpha=0.3, label='Control Cost')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim(0, 40)

# Annotate Malleable Phases 
phase_labels = [(7.5, "Instantiation"), (23, "Fusion"), (42, "Migration"), (56, "Dissolution")]
for t, text in phase_labels:
    idx = int(t * 10)
    ax1.annotate(text, xy=(t, powers[idx]), xytext=(t, 4200),
                 ha='center', arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=10, fontweight='bold')

#plt.title('Quantifying Control Plane Overhead in Malleable Lifecycle Stages', fontsize=14)
fig.tight_layout()
plt.show()
