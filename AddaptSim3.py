"""
Simulation 3:
Project Malleability Energy Aware in Computing Continuum
By @carlosjaimebh and Betico
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
for scenario, base_power in POW_

