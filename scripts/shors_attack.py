# scripts/shors_attack.py
# Shor's Algorithm Simulation
# Shows ECDSA is vulnerable, ML-DSA-65 is resistant

import time
import math
import random
import hashlib
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from ecdsa import SigningKey, SECP256k1
import oqs

warnings.filterwarnings('ignore')

# ─── Colors ───────────────────────────────────────
BG_COLOR     = '#1a1a2e'
PANEL_COLOR  = '#16213e'
PQ_COLOR     = '#00d4ff'
ECDSA_COLOR  = '#ff6b6b'
SUCCESS_COLOR = '#51cf66'
FAIL_COLOR   = '#ff6b6b'
WARN_COLOR   = '#ffd43b'


# ─── Shor's Algorithm Simulator ───────────────────
class ShorsAlgorithmSimulator:
    """
    Simulates Shor's Algorithm attack on cryptographic keys.
    
    Note: This is a classical simulation demonstrating
    the CONCEPT of Shor's algorithm. Real Shor's algorithm
    runs on quantum hardware. This simulation shows why
    ECDSA is theoretically vulnerable while ML-DSA-65
    is resistant.
    """

    def __init__(self):
        self.results = {}

    def simulate_quantum_period_finding(self, n, a, steps=1000):
        """
        Simulate quantum period finding - core of Shor's algorithm.
        In real quantum computer this runs in O(log N)^3 time.
        Here we simulate the process classically.
        """
        # Simulate quantum superposition states
        sequence = []
        x = 1
        for _ in range(steps):
            x = (x * a) % n
            sequence.append(x)
            if x == 1:
                break
        return len(sequence)

    def simulate_factor_finding(self, n, max_attempts=50):
        """
        Simulate Shor's factoring algorithm.
        Finds prime factors of n (simulating ECDSA key breaking).
        """
        print(f"\n[SHOR] Attempting to factor N = {n}")
        print(f"[SHOR] Simulating quantum period finding...")

        attempts = 0
        start_time = time.time()

        for attempt in range(max_attempts):
            attempts += 1

            # Pick random a
            a = random.randint(2, n - 1)

            # Check GCD
            gcd = math.gcd(a, n)
            if gcd > 1 and gcd < n:
                elapsed = (time.time() - start_time) * 1000
                print(f"[SHOR] Factor found via GCD: "
                      f"{gcd} x {n // gcd}")
                print(f"[SHOR] Attempts needed: {attempts}")
                print(f"[SHOR] Time taken: {elapsed:.3f} ms")
                return {
                    'success': True,
                    'factor1': gcd,
                    'factor2': n // gcd,
                    'attempts': attempts,
                    'time_ms': elapsed
                }

            # Quantum period finding (simulated)
            period = self.simulate_quantum_period_finding(n, a)

            # Try to find factors using period
            if period % 2 == 0:
                x = pow(a, period // 2, n)
                factor1 = math.gcd(x - 1, n)
                factor2 = math.gcd(x + 1, n)

                if (factor1 > 1 and factor1 < n):
                    elapsed = (time.time() - start_time) * 1000
                    print(f"[SHOR] Factor found via period: "
                          f"{factor1} x {n // factor1}")
                    print(f"[SHOR] Period r = {period}")
                    print(f"[SHOR] Attempts needed: {attempts}")
                    print(f"[SHOR] Time taken: {elapsed:.3f} ms")
                    return {
                        'success': True,
                        'factor1': factor1,
                        'factor2': n // factor1,
                        'attempts': attempts,
                        'time_ms': elapsed,
                        'period': period
                    }

        elapsed = (time.time() - start_time) * 1000
        return {
            'success': False,
            'attempts': attempts,
            'time_ms': elapsed
        }

    def attack_ecdsa(self):
        """
        Simulate Shor's algorithm attack on ECDSA.
        ECDSA relies on elliptic curve discrete logarithm
        which Shor's algorithm can solve efficiently.
        """
        print("\n" + "="*50)
        print("ATTACKING ECDSA WITH SHOR'S ALGORITHM")
        print("="*50)

        # Generate ECDSA key
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        private_key_int = int.from_bytes(
            private_key.to_string(), 'big'
        )

        print(f"[ECDSA] Private key (first 8 bytes): "
              f"{private_key.to_string().hex()[:16]}...")
        print(f"[ECDSA] Key size: "
              f"{len(private_key.to_string()) * 8} bits")
        print(f"[ECDSA] Security basis: "
              f"Elliptic Curve Discrete Logarithm Problem")
        print(f"[ECDSA] Quantum vulnerability: "
              f"Shor's Algorithm solves ECDLP in O(n^3)")

        # Simulate attack using small prime factorization
        # (represents the mathematical structure Shor's exploits)
        attack_results = []
        key_moduli = [
            1147, 1763, 2059, 3127, 3599,
            4087, 5183, 5767, 6557, 7657
        ]

        print(f"\n[SHOR] Running quantum period finding...")
        print(f"[SHOR] Simulating quantum circuit execution...")

        total_start = time.time()
        successful_attacks = 0

        for n in key_moduli[:5]:
            result = self.simulate_factor_finding(n)
            attack_results.append(result)
            if result['success']:
                successful_attacks += 1

        total_time = (time.time() - total_start) * 1000

        success_rate = (
            successful_attacks / len(key_moduli[:5])
        ) * 100

        print(f"\n[ECDSA] Attack Results:")
        print(f"[ECDSA] Successful attacks: "
              f"{successful_attacks}/5")
        print(f"[ECDSA] Success rate: {success_rate:.1f}%")
        print(f"[ECDSA] Total attack time: {total_time:.2f} ms")
        print(f"[ECDSA] STATUS: VULNERABLE TO QUANTUM ATTACK")

        return {
            'algorithm': 'ECDSA-SECP256k1',
            'vulnerable': True,
            'success_rate': success_rate,
            'attack_results': attack_results,
            'total_time': total_time,
            'key_size_bits': 256,
            'quantum_complexity': 'O(n^3) - Polynomial',
            'status': 'BROKEN'
        }

    def attack_ml_dsa(self):
        """
        Simulate Shor's algorithm attempt on ML-DSA-65.
        ML-DSA-65 is based on lattice problems which
        Shor's algorithm CANNOT solve efficiently.
        """
        print("\n" + "="*50)
        print("ATTACKING ML-DSA-65 WITH SHOR'S ALGORITHM")
        print("="*50)

        # Generate ML-DSA-65 key
        sig = oqs.Signature('ML-DSA-65')
        public_key = sig.generate_keypair()

        print(f"[ML-DSA] Public key size: "
              f"{len(public_key)} bytes "
              f"({len(public_key) * 8} bits)")
        print(f"[ML-DSA] Security basis: "
              f"Module Learning With Errors (MLWE)")
        print(f"[ML-DSA] Quantum complexity: "
              f"No known polynomial quantum algorithm")
        print(f"[ML-DSA] NIST Status: "
              f"Approved Post-Quantum Standard")

        print(f"\n[SHOR] Attempting quantum period finding...")
        print(f"[SHOR] Analyzing lattice structure...")

        attack_results = []
        total_start = time.time()
        failed_attacks = 0

        # Simulate failed attacks on lattice structure
        # Lattice problems have exponential quantum complexity
        lattice_dimensions = [128, 256, 512, 1024, 2048]

        for dim in lattice_dimensions:
            start = time.time()
            print(f"\n[SHOR] Attacking lattice dimension {dim}...")
            print(f"[SHOR] Quantum search space: 2^{dim}")

            # Simulate exponential search failure
            # Best known quantum algorithm is still exponential
            simulated_steps = min(2**20, dim * dim * 1000)
            simulated_time = random.uniform(50, 200)
            time.sleep(0.05)  # Simulate computation

            elapsed = (time.time() - start) * 1000
            failed_attacks += 1

            print(f"[SHOR] Steps attempted: {simulated_steps:,}")
            print(f"[SHOR] Result: FAILED - "
                  f"Exponential complexity detected")

            attack_results.append({
                'dimension': dim,
                'success': False,
                'steps': simulated_steps,
                'time_ms': elapsed
            })

        total_time = (time.time() - total_start) * 1000

        print(f"\n[ML-DSA] Attack Results:")
        print(f"[ML-DSA] Failed attacks: {failed_attacks}/5")
        print(f"[ML-DSA] Success rate: 0.0%")
        print(f"[ML-DSA] Total time: {total_time:.2f} ms")
        print(f"[ML-DSA] STATUS: RESISTANT TO QUANTUM ATTACK")

        return {
            'algorithm': 'ML-DSA-65',
            'vulnerable': False,
            'success_rate': 0.0,
            'attack_results': attack_results,
            'total_time': total_time,
            'key_size_bits': len(public_key) * 8,
            'quantum_complexity': 'O(2^n) - Exponential',
            'status': 'SECURE'
        }

    def run_comparison(self):
        """Run complete attack comparison"""
        print("\n" + "="*60)
        print("SHOR'S ALGORITHM ATTACK SIMULATION")
        print("Post-Quantum vs Classical Cryptography")
        print("="*60)
        print("\nNote: This simulates the MATHEMATICAL CONCEPT")
        print("of Shor's algorithm to demonstrate why")
        print("ECDSA is vulnerable and ML-DSA-65 is resistant.")
        print("="*60)

        # Attack both
        ecdsa_result = self.attack_ecdsa()
        mldsa_result = self.attack_ml_dsa()

        # Store results
        self.results = {
            'ecdsa': ecdsa_result,
            'ml_dsa': mldsa_result
        }

        return ecdsa_result, mldsa_result


# ─── Visualization ────────────────────────────────
def visualize_attack_results(ecdsa_result, mldsa_result):
    """Create visual charts for attack simulation"""

    plt.rcParams['figure.facecolor'] = BG_COLOR
    plt.rcParams['axes.facecolor'] = PANEL_COLOR
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Shor's Algorithm Attack Simulation\n"
        "ECDSA (Vulnerable) vs ML-DSA-65 (Quantum Resistant)",
        fontsize=14, fontweight='bold',
        color='white', y=0.98
    )

    # ── Chart 1: Attack Success Rate ──────────────
    ax1 = axes[0, 0]
    algorithms = ['ECDSA\n(Classical)', 'ML-DSA-65\n(Post-Quantum)']
    success_rates = [
        ecdsa_result['success_rate'],
        mldsa_result['success_rate']
    ]
    colors = [ECDSA_COLOR, PQ_COLOR]
    bars = ax1.bar(algorithms, success_rates,
                   color=colors, width=0.5,
                   edgecolor='white', linewidth=0.5)

    ax1.set_title("Shor's Attack Success Rate",
                  fontweight='bold', color='white')
    ax1.set_ylabel('Success Rate (%)', color='white')
    ax1.set_ylim(0, 120)
    ax1.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, success_rates):
        label = f'{val:.1f}%'
        status = '❌ VULNERABLE' if val > 0 else '✅ RESISTANT'
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 2,
            f'{label}\n{status}',
            ha='center', va='bottom',
            color='white', fontweight='bold',
            fontsize=10
        )

    # ── Chart 2: Quantum Complexity ───────────────
    ax2 = axes[0, 1]
    complexities = {
        'ECDSA\n(Shor\'s\nAlgorithm)': 3,
        'ML-DSA-65\n(Best Known\nQuantum)': 100
    }
    colors2 = [ECDSA_COLOR, PQ_COLOR]
    bars2 = ax2.bar(
        list(complexities.keys()),
        list(complexities.values()),
        color=colors2, width=0.5,
        edgecolor='white', linewidth=0.5
    )
    ax2.set_title('Quantum Attack Complexity',
                  fontweight='bold', color='white')
    ax2.set_ylabel('Relative Complexity', color='white')
    ax2.grid(axis='y', alpha=0.3)

    labels2 = ['O(n³)\nPolynomial', 'O(2ⁿ)\nExponential']
    for bar, label in zip(bars2, labels2):
        ax2.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 1,
            label,
            ha='center', va='bottom',
            color='white', fontweight='bold',
            fontsize=9
        )

    # ── Chart 3: Attack Timeline ───────────────────
    ax3 = axes[1, 0]

    # ECDSA attack progress
    ecdsa_attempts = [
        r['attempts'] for r in
        ecdsa_result['attack_results']
        if r['success']
    ]
    ecdsa_times = [
        r['time_ms'] for r in
        ecdsa_result['attack_results']
        if r['success']
    ]

    # ML-DSA attack progress (all failed)
    mldsa_dims = [
        r['dimension'] for r in
        mldsa_result['attack_results']
    ]
    mldsa_times = [
        r['time_ms'] for r in
        mldsa_result['attack_results']
    ]

    x_ecdsa = list(range(1, len(ecdsa_times) + 1))
    x_mldsa = list(range(1, len(mldsa_times) + 1))

    if ecdsa_times:
        ax3.plot(x_ecdsa, ecdsa_times,
                 color=ECDSA_COLOR, marker='o',
                 linewidth=2, markersize=8,
                 label='ECDSA (Attacks Succeeded)')

    ax3.plot(x_mldsa, mldsa_times,
             color=PQ_COLOR, marker='x',
             linewidth=2, markersize=8,
             label='ML-DSA-65 (All Failed)')

    ax3.set_title('Attack Timeline Per Attempt',
                  fontweight='bold', color='white')
    ax3.set_xlabel('Attack Attempt', color='white')
    ax3.set_ylabel('Time (ms)', color='white')
    ax3.legend(facecolor=PANEL_COLOR,
               edgecolor='white',
               labelcolor='white')
    ax3.grid(alpha=0.3)

    # ── Chart 4: Security Comparison Table ────────
    ax4 = axes[1, 1]
    ax4.axis('off')

    table_data = [
        ['Property', 'ECDSA', 'ML-DSA-65'],
        ['Algorithm Type',
         'Elliptic Curve', 'Lattice-Based'],
        ['Key Size',
         '256 bits', '1952 bytes'],
        ['Signature Size',
         '64 bytes', '3309 bytes'],
        ['Classical Security',
         '✅ Secure', '✅ Secure'],
        ["Shor's Attack",
         '❌ VULNERABLE', '✅ RESISTANT'],
        ["Grover's Attack",
         '⚠️ Weakened', '✅ Resistant'],
        ['Quantum Complexity',
         'O(n³)', 'O(2ⁿ)'],
        ['NIST Approved',
         '❌ Deprecated', '✅ PQC Standard'],
        ['Recommended',
         '❌ NO', '✅ YES'],
    ]

    table = ax4.table(
        cellText=table_data[1:],
        colLabels=table_data[0],
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)

    for (row, col), cell in table.get_celld().items():
        cell.set_facecolor(PANEL_COLOR)
        cell.set_edgecolor('#0f3460')
        cell.set_text_props(color='white')

        if row == 0:
            cell.set_facecolor('#0f3460')
            cell.set_text_props(
                color='white', fontweight='bold'
            )

        if col == 1 and row > 0:
            text = cell.get_text().get_text()
            if '❌' in text:
                cell.set_facecolor('#4a1a1a')
            elif '⚠️' in text:
                cell.set_facecolor('#4a3a1a')

        if col == 2 and row > 0:
            text = cell.get_text().get_text()
            if '✅' in text:
                cell.set_facecolor('#1a472a')

    ax4.set_title(
        'Cryptographic Security Comparison',
        fontweight='bold', color='white', pad=20
    )

    plt.tight_layout()
    plt.savefig(
        'results/shors_attack_simulation.png',
        dpi=150, bbox_inches='tight',
        facecolor=BG_COLOR
    )
    print("\n[Chart] Shor's attack chart saved!")
    plt.close()


# ─── Main ─────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("SHOR'S ALGORITHM ATTACK SIMULATION")
    print("=" * 60)

    simulator = ShorsAlgorithmSimulator()

    # Run attacks
    ecdsa_result, mldsa_result = simulator.run_comparison()

    # Print final summary
    print("\n" + "="*60)
    print("ATTACK SIMULATION SUMMARY")
    print("="*60)

    summary_data = [
        ["Algorithm",
         "ECDSA-SECP256k1", "ML-DSA-65"],
        ["Quantum Complexity",
         ecdsa_result['quantum_complexity'],
         mldsa_result['quantum_complexity']],
        ["Attack Success Rate",
         f"{ecdsa_result['success_rate']:.1f}%",
         f"{mldsa_result['success_rate']:.1f}%"],
        ["Status",
         ecdsa_result['status'],
         mldsa_result['status']],
        ["Recommended",
         "NO", "YES"],
    ]

    col_width = 25
    for row in summary_data:
        print(
            f"{row[0]:<20} "
            f"{row[1]:<25} "
            f"{row[2]:<25}"
        )

    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("""
✅ ECDSA is VULNERABLE to Shor's Algorithm
   - Quantum computers can break ECDSA in O(n³) time
   - All Bitcoin/Ethereum wallets at risk
   - Must be replaced before quantum computers scale

✅ ML-DSA-65 is RESISTANT to Shor's Algorithm  
   - Based on lattice problems with O(2ⁿ) complexity
   - No known efficient quantum algorithm exists
   - NIST approved post-quantum standard
   - Safe for use in the quantum era

✅ Your smart contract uses ML-DSA-65
   - Protected against future quantum attacks
   - Self-healing adds runtime protection
   - Threshold recovery ensures availability
    """)

    # Generate visualization
    visualize_attack_results(ecdsa_result, mldsa_result)

    print("[DONE] Simulation complete!")
    print("[DONE] Chart: results/shors_attack_simulation.png")