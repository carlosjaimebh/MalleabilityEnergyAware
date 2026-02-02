"""
Project Malleability Energy Aware in Contiuum Computing
@carlosjaimebh and @betico

Simulation 2:
Per-node energy breakdown for a 4-node Jetson Nano 2GB millicluster
running MLPerf Inference-inspired workloads, extended with
DVFS / throttling policies.
"""

import random
import matplotlib.pyplot as plt

# -------------------------------
# Reproducibility
# -------------------------------
random.seed(11)

# -------------------------------
# Cluster configuration
# -------------------------------
NODES = ["Node 1", "Node 2", "Node 3", "Node 4"]

# MLPerf Inference-inspired power profiles (Watts per node)
# - Edge ≈ SingleStream
# - Offline ≈ Offline
POWER_PROFILES = {
    "Edge": 4.0,      # latency-oriented inference
    "Offline": 6.5    # throughput-oriented inference
}

# DVFS / throttling policies (scaling factors)
DVFS_POLICIES = {
    "No_DVFS": 1.0,          # baseline performance
    "Energy_Saver": 0.8,     # aggressive DVFS
    "Thermal_Limit": 0.9    # mild thermal throttling
}

# Adaptation lifecycle stages (seconds)
STAGES = {
    "Instantiation": 30,
    "Fusion": 45,
    "Dissolution": 20,
    "Migration": 35
}

# -------------------------------
# Energy data structure
# energy[scenario][policy][stage][node] = Joules
# -------------------------------
energy = {
    scenario: {
        policy: {stage: {} for stage in STAGES}
        for policy in DVFS_POLICIES
    }
    for scenario in POWER_PROFILES
}

# -------------------------------
# Simulation loop
# -------------------------------
for scenario, base_power in POWER_PROFILES.items():
    for policy, dvfs_scale in DVFS_POLICIES.items():
        for stage, duration in STAGES.items():
            for node in NODES:
                # Node-level variability (heterogeneity, thermal effects)
                node_variability = random.uniform(0.85, 1.15)

                effective_power = base_power * dvfs_scale
                energy_consumed = effective_power * duration * node_variability

                energy[scenario][policy][stage][node] = energy_consumed

# -------------------------------
# Aggregate energy per stage
# (Edge / SingleStream shown)
# -------------------------------
edge_no_dvfs = [
    sum(energy["Edge"]["No_DVFS"][stage].values()) for stage in STAGES
]
edge_energy_saver = [
    sum(energy["Edge"]["Energy_Saver"][stage].values()) for stage in STAGES
]
edge_thermal_limit = [
    sum(energy["Edge"]["Thermal_Limit"][stage].values()) for stage in STAGES
]

# -------------------------------
# Plot DVFS impact
# -------------------------------
x = range(len(STAGES))

plt.figure()
plt.bar(x, edge_no_dvfs, width=0.25, label="No DVFS")
plt.bar([i + 0.25 for i in x], edge_energy_saver, width=0.25, label="Energy Saver DVFS")
plt.bar([i + 0.5 for i in x], edge_thermal_limit, width=0.25, label="Thermal Limit DVFS")

plt.xticks([i + 0.25 for i in x], list(STAGES.keys()))
plt.xlabel("Lifecycle Stage")
plt.ylabel("Energy Consumption (Joules)")
plt.title(
    "Impact of DVFS / Throttling Policies on Energy Consumption\n"
    "MLPerf SingleStream (Edge), 4× Jetson Nano 2GB"
)
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------------
# Print detailed per-node breakdown
# -------------------------------
print("\nPer-node energy consumption (Edge scenario):")
for policy in DVFS_POLICIES:
    print(f"\nDVFS Policy: {policy}")
    for stage in STAGES:
        print(f"  {stage}:")
        for node, value in energy["Edge"][policy][stage].items():
            print(f"    {node}: {value:.2f} J")

