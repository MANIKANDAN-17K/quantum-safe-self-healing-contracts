# Quantum-Safe Self-Healing Smart Contracts

> Threshold-Based Self-Healing Smart Contracts with Post-Quantum Signatures for Secure DeFi Financial Transactions

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.19-orange.svg)](https://soliditylang.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-purple.svg)](https://ethereum.org)
[![PQC](https://img.shields.io/badge/PQC-ML--DSA--65-red.svg)](https://openquantumsafe.org)

---

## Overview

This project implements a **Threshold-Based Self-Healing Smart Contract** system that combines:

- **Post-Quantum Cryptography** (ML-DSA-65 / Dilithium3) to protect against future quantum computer attacks
- **Autonomous Self-Healing** that automatically detects attacks and recovers without manual intervention
- **Threshold-Based Recovery** — a novel mechanism where the contract decides itself when to resume after being paused

### The Problem

| Threat | Classical Blockchain | This Project |
|--------|---------------------|--------------|
| Shor's Algorithm |  ECDSA broken | ML-DSA-65 resistant |
| Smart Contract Bugs |  No auto-recovery |  Auto-heals itself |
| Manual Recovery |  Hours of downtime | Seconds, no admin needed |

---

## Novel Contribution

> **Threshold-Based Automatic Recovery** — the contract autonomously resumes operations after detecting N consecutive safe transactions, without any manual administrator intervention. This is the first implementation combining post-quantum signatures with fully automatic threshold-based contract recovery for DeFi financial transactions.

---

## Key Results

| Metric | ML-DSA-65 (PQ) | ECDSA (Classical) |
|--------|---------------|-------------------|
| Avg Sign Time | 0.312 ms | 0.864 ms |
| Avg Verify Time | 0.089 ms | 3.288 ms |
| Quantum Safe | Yes |  No |
| Auto Recovery | Yes |  No |

- PQ signatures are **2.7x faster** to sign than ECDSA
- PQ signatures are **36x faster** to verify than ECDSA
- Contract auto-pauses after **3 attacks** (threshold)
- Contract auto-recovers after **5 safe transactions** (novel)
- Average recovery time: **28.7 ms** (vs hours in traditional systems)

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│              User / DeFi Application         │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│         Post-Quantum Signature Layer         │
│         ML-DSA-65 (CRYSTALS-Dilithium)       │
│         Sign → Verify → Pass/Fail            │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│         Smart Contract Layer                 │
│         Solidity 0.8.19 + OpenZeppelin       │
│                                              │
│  ┌─────────────┐    ┌──────────────────────┐│
│  │  Transfer   │    │   Self-Healing Logic  ││
│  │  Function   │───▶│   Attack Counter      ││
│  └─────────────┘    │   Auto-Pause          ││
│                     │   Threshold Recovery  ││
│                     └──────────────────────┘│
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│         Blockchain Layer                     │
│         Ethereum (Ganache Local)             │
│         Chain ID: 1337                       │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
quantum-safe-self-healing-contracts/
│
├── contracts/
│   └── QuantumSafeContract.sol      # Main smart contract
│
├── scripts/
│   ├── deploy_contract.py           # Deploy to Ganache
│   ├── pq_sign.py                   # PQ signing module
│   └── ecdsa_sign.py                # ECDSA comparison module
│
├── monitoring/
│   └── attack_simulator.py          # Attack + healing demo
│
├── results/
│   ├── performance_metrics.py       # Performance analysis
│   ├── visualize.py                 # Charts and graphs
│   ├── simulation_results.json      # Raw results
│   └── final_report.json            # Summary report
│
├── main.py                          # Run complete demo
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## Installation

### Prerequisites

- Ubuntu 20.04+ / Windows WSL2
- Python 3.10+
- Node.js 18+
- 8GB RAM minimum

### Step 1 — Clone Repository

```bash
git clone https://github.com/yourusername/quantum-safe-self-healing-contracts.git
cd quantum-safe-self-healing-contracts
```

### Step 2 — Install liboqs C Library

```bash
sudo apt install -y cmake gcc g++ python3-dev libssl-dev ninja-build
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -GNinja -DBUILD_SHARED_LIBS=ON ..
ninja
sudo ninja install
sudo ldconfig
cd ../..
```

### Step 3 — Create Virtual Environment

```bash
python3 -m venv qsc_env
source qsc_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4 — Install Ganache

```bash
npm install -g ganache
```

---

## Running the Project

### Step 1 — Start Ganache (New Terminal)

```bash
ganache --port 8545 --accounts 10 --deterministic
```

### Step 2 — Deploy Contract

```bash
source qsc_env/bin/activate
python3 scripts/deploy_contract.py
```

### Step 3 — Run Attack Simulation

```bash
python3 monitoring/attack_simulator.py
```

### Step 4 — Generate Performance Report

```bash
python3 results/performance_metrics.py
```

### Step 5 — Generate Visual Charts

```bash
python3 results/visualize.py
```

### Or Run Everything at Once

```bash
python3 main.py
```

---

## Demo Flow

```
Phase 1: PQ vs ECDSA Comparison
        ↓
Phase 2: Normal Valid Transactions (3 tx)
        ↓
Phase 3: Attack Simulation (3 attacks)
        ↓ Contract Auto-Pauses!
Phase 4: Threshold-Based Auto Recovery (5 safe tx)
        ↓ Contract Auto-Recovers! (Novel)
Phase 5: Resumed Normal Operations (3 tx)
        ↓
Results: Performance Metrics + Charts
```

---

## Smart Contract Features

### Self-Healing Mechanism

```solidity
// Auto-pause after 3 attacks
if (attackCount >= ATTACK_THRESHOLD) {
    paused = true;
    emit ContractPaused("Auto-paused", attackCount);
}

// Auto-recover after 5 safe transactions
if (safeTransactionCount >= RECOVERY_THRESHOLD) {
    paused = false;
    autoRecoveryCount++;
    emit ContractResumed("AUTO-RECOVERY", safeCount);
}
```

### Key Contract Functions

| Function | Description |
|----------|-------------|
| `transfer()` | PQ-verified fund transfer |
| `attemptAutoRecovery()` | Threshold-based auto recovery |
| `manualRecovery()` | Admin override recovery |
| `emergencyPause()` | Admin emergency stop |
| `getContractStatus()` | Full system status |

---

## Security Analysis

| Attack Type | Classical | This Project |
|-------------|-----------|--------------|
| Shor's Algorithm |  Breaks ECDSA |  ML-DSA-65 resistant |
| Grover's Algorithm |  Weakens hashing |  Resistant |
| Replay Attack | Possible | Blocked |
| Signature Forgery |  Quantum possible |  Not possible |
| Reentrancy Attack |  Vulnerable |  Self-heals |
| DoS Attack |  Contract breaks |  Auto-pauses |

---

## Generated Charts

| Chart | Description |
|-------|-------------|
| chart1_signature_comparison.png | PQ vs ECDSA performance |
| chart2_attack_healing.png | Attack simulation + recovery |
| chart3_summary.png | Security radar + metrics table |
| chart4_timeline.png | Complete system timeline |

---

## Requirements

```
web3>=6.0.0
py-solc-x>=2.0.0
liboqs-python>=0.7.0
ecdsa>=0.18.0
matplotlib>=3.7.0
numpy>=1.24.0
tabulate>=0.9.0
cryptography>=41.0.0
```

---

## Future Work

- [ ] IBM Quantum hardware validation (Shor's attack demo)
- [ ] On-chain PQ verification using ZK-proofs
- [ ] Adaptive ML-based dynamic thresholds
- [ ] Multi-chain deployment (Polygon, BSC)
- [ ] Real DeFi protocol integration (Uniswap, Aave)
- [ ] QSDC integration for physics-based security
- [ ] IoT lightweight version
- [ ] Formal security verification

---

## Research Paper

This project is based on and extends:

> Sun et al., "Quantum Blockchain Relying on Quantum Secure Direct Communication Network," IEEE Internet of Things Journal, Vol. 12, No. 10, May 2025.

**Novel contributions over existing work:**
1. Threshold-based automatic recovery (no manual intervention)
2. PQ + self-healing combination for DeFi
3. Performance benchmark: PQ vs ECDSA comparison
4. Autonomous attack detection and response

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

## Author

**Manikandan**
- Project: Quantum-Safe Self-Healing Smart Contracts
- Institution: Anna University
- Year: 2026

---

## Acknowledgments

- [Open Quantum Safe](https://openquantumsafe.org/) — liboqs library
- [OpenZeppelin](https://openzeppelin.com/) — Smart contract templates
- [Truffle Suite](https://trufflesuite.com/) — Ganache blockchain simulator
- IEEE IoT Journal — Paper 4 (Sun et al., 2025)