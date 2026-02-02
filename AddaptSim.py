"""
Project Malleability Energy Aware in Contiuum Computing
@carlosjaimebh and @betico
Simulation 1:
Lifecycle energy consumption for a 4-node Jetson Nano millicluster
running a simple MLPerf-like workload.
"""

import random
import matplotlib.pyplot as plt

# Reproducibility
random.seed(42)

# Cluster parameters
NUM_NODES = 4
BASE_POWER_WATTS = 5.0  # average Jetson Nano 2GB power under ML load

# Lifecycle stages (seconds)
STAGES = {
    "Instantiation": 30,
    "Fusion": 45,
    "Dissolution": 20,
    "Migration": 35
}

# Energy computation
energy_by_stage = {}

for stage, duration in STAGES.items():
    variability = random.uniform(0.9, 1.1)
    energy = NUM_NODES * BASE_POWER_WATTS * duration * variability
    energy_by_stage[stage] = energy

# Plot
plt.figure()
plt.bar(energy_by_stage.keys(), energy_by_stage.values())
plt.xlabel("Lifecycle Stage")
plt.ylabel("Energy Consumption (Joules)")
plt.title("Energy Consumption by Lifecycle Stage\n4× Jetson Nano 2GB (MLPerf Simulation)")
plt.tight_layout()
plt.show()

print("Energy by stage (Joules):")
for stage, energy in energy_by_stage.items():
    print(f"{stage}: {energy:.2f} J")


















