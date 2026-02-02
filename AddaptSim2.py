"""
Project Malleablity Energy Aware in Continuum Computing
@carlosjaimebh and Betico
Simulation 2:
Per-node energy breakdown with MLPerf Edge vs Offline scenarios
for a 4-node Jetson Nano 2GB millicluster.
"""

import random
import matplotlib.pyplot as plt

# Reproducibility
random.seed(7)

# Nodes
NODES = ["Node 1", "Node 2", "Node 3", "Node 4"]

# MLPerf power profiles (Watts per node)
POWER_PROFILES = {
    "Edge": 4.0,     # lighter inference workload
    "Offline": 6.5   # heavier batch-style workload
}

# Lifecycle stages (seconds)
STAGES = {
    "Instantiation": 30,
    "Fusion": 45,
    "Dissolution": 20,
    "Migration": 35
}

# Energy data structure
# energy[scenario][stage][node] = Joules
energy = {
    scenario: {stage: {} for stage in STAGES}
    for scenario in POWER_PROFILES
}

# Simulation
for scenario, base_power in POWER_PROFILES.items():
    for stage, duration in STAGES.items():
        for node in NODES:
            node_variability = random.uniform(0.85, 1.15)
            energy[scenario][stage][node] = (
                base_power * duration * node_variability
            )

# Aggregate per-stage energy
edge_energy = [
    sum(energy["Edge"][stage].values()) for stage in STAGES
]
offline_energy = [
    sum(energy["Offline"][stage].values()) for stage in STAGES
]

# Plot
x = range(len(STAGES))
plt.figure()
plt.bar(x, edge_energy, width=0.4, label="MLPerf Edge", align="center")
plt.bar([i + 0.4 for i in x], offline_energy, width=0.4, label="MLPerf Offline", align="center")

plt.xticks([i + 0.2 for i in x], list(STAGES.keys()))
plt.xlabel("Lifecycle Stage")
plt.ylabel("Energy Consumption (Joules)")
plt.title(
    "Energy Consumption by Stage and MLPerf Scenario\n"
    "Per-node Aggregated (4× Jetson Nano 2GB)"
)
plt.legend()
plt.tight_layout()
plt.show()

# Print detailed per-node energy
print("\nDetailed per-node energy consumption (Joules):")
for scenario in energy:
    print(f"\nScenario: {scenario}")
    for stage in energy[scenario]:
        print(f"  {stage}:")
        for node, value in energy[scenario][stage].items():
            print(f"    {node}: {value:.2f} J")

