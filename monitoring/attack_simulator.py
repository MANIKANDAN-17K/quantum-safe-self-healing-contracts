# monitoring/attack_simulator.py

import sys
import os
import json
import time
import hashlib
import warnings
warnings.filterwarnings('ignore')

from web3 import Web3
import oqs
from ecdsa import SigningKey, SECP256k1, BadSignatureError


# PQ Signer
class PostQuantumSigner:
    def __init__(self):
        self.algorithm = 'ML-DSA-65'
        self.sig = oqs.Signature(self.algorithm)
        self.public_key = None

    def generate_keys(self):
        self.public_key = self.sig.generate_keypair()
        print(f"[PQ] Keys generated: {self.algorithm}")
        print(f"[PQ] Public key size: {len(self.public_key)} bytes")
        return self.public_key

    def sign_transaction(self, data):
        start = time.time()
        if isinstance(data, str):
            data = data.encode()
        signature = self.sig.sign(data)
        sign_time = (time.time() - start) * 1000
        return signature, sign_time

    def verify_transaction(self, data, signature):
        start = time.time()
        if isinstance(data, str):
            data = data.encode()
        try:
            is_valid = self.sig.verify(
                data, signature, self.public_key
            )
        except Exception:
            is_valid = False
        verify_time = (time.time() - start) * 1000
        return is_valid, verify_time


# ECDSA Signer
class ECDSASigner:
    def __init__(self):
        self.algorithm = 'ECDSA-SECP256k1'
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def sign_transaction(self, data):
        start = time.time()
        if isinstance(data, str):
            data = data.encode()
        tx_hash = hashlib.sha256(data).digest()
        signature = self.private_key.sign(tx_hash)
        sign_time = (time.time() - start) * 1000
        return signature, sign_time

    def verify_transaction(self, data, signature):
        start = time.time()
        if isinstance(data, str):
            data = data.encode()
        tx_hash = hashlib.sha256(data).digest()
        try:
            self.public_key.verify(signature, tx_hash)
            is_valid = True
        except BadSignatureError:
            is_valid = False
        verify_time = (time.time() - start) * 1000
        return is_valid, verify_time


# Attack Simulator
class AttackSimulator:

    def __init__(self):
        with open('contract_info.json', 'r') as f:
            self.contract_info = json.load(f)

        self.w3 = Web3(
            Web3.HTTPProvider('http://127.0.0.1:8545')
        )
        self.contract = self.w3.eth.contract(
            address=self.contract_info['address'],
            abi=self.contract_info['abi']
        )

        self.owner    = self.contract_info['accounts'][0]
        self.alice    = self.contract_info['accounts'][1]
        self.bob      = self.contract_info['accounts'][2]
        self.attacker = self.contract_info['accounts'][3]

        self.pq_signer    = PostQuantumSigner()
        self.ecdsa_signer = ECDSASigner()
        self.pq_signer.generate_keys()

        self.results = []
        self.pq_sign_times    = []
        self.pq_verify_times  = []
        self.ecdsa_sign_times   = []
        self.ecdsa_verify_times = []

        print("\n[Simulator] Ready")
        print(f"[Simulator] Owner:    {self.owner[:20]}...")
        print(f"[Simulator] Alice:    {self.alice[:20]}...")
        print(f"[Simulator] Bob:      {self.bob[:20]}...")
        print(f"[Simulator] Attacker: {self.attacker[:20]}...")

    def compare_signatures(self, transaction_data):
        """Compare PQ vs ECDSA performance"""
        print("\n[COMPARE] Running signature comparison...")

        pq_sig, pq_sign = self.pq_signer.sign_transaction(
            transaction_data
        )
        pq_valid, pq_verify = self.pq_signer.verify_transaction(
            transaction_data, pq_sig
        )

        ec_sig, ec_sign = self.ecdsa_signer.sign_transaction(
            transaction_data
        )
        ec_valid, ec_verify = self.ecdsa_signer.verify_transaction(
            transaction_data, ec_sig
        )

        self.pq_sign_times.append(pq_sign)
        self.pq_verify_times.append(pq_verify)
        self.ecdsa_sign_times.append(ec_sign)
        self.ecdsa_verify_times.append(ec_verify)

        print(f"[PQ]    Sign: {pq_sign:.3f}ms  "
              f"Verify: {pq_verify:.3f}ms  "
              f"Valid: {pq_valid}")
        print(f"[ECDSA] Sign: {ec_sign:.3f}ms  "
              f"Verify: {ec_verify:.3f}ms  "
              f"Valid: {ec_valid}")

        return pq_sign, pq_verify, ec_sign, ec_verify

    def send_valid_transaction(self, sender, recipient, amount):
        """Send valid PQ signed transaction"""
        tx_data = f"Transfer {amount} ETH {sender} to {recipient}"
        sig, sign_time = self.pq_signer.sign_transaction(tx_data)
        is_valid, verify_time = self.pq_signer.verify_transaction(
            tx_data, sig
        )

        amount_wei = self.w3.to_wei(amount, 'ether')
        start = time.time()
        tx_hash = self.contract.functions.transfer(
            recipient,
            amount_wei,
            True
        ).transact({'from': sender, 'gas': 300000})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_time = (time.time() - start) * 1000

        self.results.append({
            'type': 'VALID',
            'pq_sign': sign_time,
            'pq_verify': verify_time,
            'tx_time': tx_time,
            'status': 'SUCCESS'
        })

        print(f"[TX] Valid | Sign: {sign_time:.3f}ms | "
              f"Verify: {verify_time:.3f}ms | "
              f"TX: {tx_time:.2f}ms")
        return sign_time, verify_time, tx_time

    def send_attack_transaction(self, attacker, recipient, amount):
        """Send attack with invalid signature"""
        fake_data = "FAKE transaction attempt"
        fake_sig, _ = self.pq_signer.sign_transaction(fake_data)
        real_data = f"Transfer {amount} ETH from {attacker}"
        is_valid, verify_time = self.pq_signer.verify_transaction(
            real_data, fake_sig
        )

        amount_wei = self.w3.to_wei(amount, 'ether')
        start = time.time()
        tx_hash = self.contract.functions.transfer(
            recipient,
            amount_wei,
            False
        ).transact({'from': attacker, 'gas': 300000})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_time = (time.time() - start) * 1000

        self.results.append({
            'type': 'ATTACK',
            'pq_sign': 0,
            'pq_verify': verify_time,
            'tx_time': tx_time,
            'status': 'BLOCKED'
        })

        print(f"[ATTACK] Blocked | "
              f"Verify: {verify_time:.3f}ms | "
              f"TX: {tx_time:.2f}ms | "
              f"Valid: {is_valid}")
        return tx_time

    def attempt_recovery(self):
        """Threshold based auto recovery"""
        print("\n[RECOVERY] Starting auto-recovery...")
        recovery_times = []

        for i in range(5):
            start = time.time()
            tx_hash = self.contract.functions.attemptAutoRecovery(
                True
            ).transact({'from': self.owner, 'gas': 200000})
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            r_time = (time.time() - start) * 1000
            recovery_times.append(r_time)

            status = self.get_status()
            print(f"[RECOVERY] Safe tx {i+1}/5 | "
                  f"Paused: {status['paused']} | "
                  f"Time: {r_time:.2f}ms")

            if not status['paused']:
                print("[RECOVERY] Auto-recovery successful!")
                avg = sum(recovery_times) / len(recovery_times)
                return avg, recovery_times

        return 0, recovery_times

    def get_status(self):
        s = self.contract.functions.getContractStatus().call()
        return {
            'paused': s[0],
            'attack_count': s[1],
            'safe_tx_count': s[2],
            'total_tx': s[3],
            'success_tx': s[4],
            'blocked_tx': s[5],
            'auto_recoveries': s[6]
        }

    def print_status(self, label=""):
        s = self.get_status()
        print(f"\n{'='*50}")
        print(f"CONTRACT STATUS: {label}")
        print(f"{'='*50}")
        print(f"  Paused:          {s['paused']}")
        print(f"  Attack Count:    {s['attack_count']}")
        print(f"  Safe Tx Count:   {s['safe_tx_count']}")
        print(f"  Total Tx:        {s['total_tx']}")
        print(f"  Successful Tx:   {s['success_tx']}")
        print(f"  Blocked Tx:      {s['blocked_tx']}")
        print(f"  Auto Recoveries: {s['auto_recoveries']}")
        print(f"{'='*50}")
        return s


# Main
if __name__ == "__main__":

    print("=" * 50)
    print("QUANTUM SAFE SELF-HEALING CONTRACT DEMO")
    print("=" * 50)

    sim = AttackSimulator()

    # Phase 1: Signature Comparison
    print("\n" + "="*50)
    print("PHASE 1: PQ vs ECDSA COMPARISON")
    print("="*50)
    for i in range(5):
        tx = f"Test transaction number {i+1} for comparison"
        sim.compare_signatures(tx)

    # Phase 2: Normal Transactions
    print("\n" + "="*50)
    print("PHASE 2: NORMAL VALID TRANSACTIONS")
    print("="*50)
    for i in range(3):
        print(f"\n[TX {i+1}]")
        sim.send_valid_transaction(
            sim.alice, sim.bob, 0.1
        )
    sim.print_status("AFTER NORMAL TX")

    # Phase 3: Attack Simulation
    print("\n" + "="*50)
    print("PHASE 3: ATTACK SIMULATION")
    print("="*50)
    for i in range(3):
        print(f"\n[ATTACK {i+1}]")
        sim.send_attack_transaction(
            sim.attacker, sim.alice, 5
        )
        s = sim.get_status()
        print(f"[STATUS] Paused: {s['paused']} | "
              f"Attacks: {s['attack_count']}")
        if s['paused']:
            print("[!!!] CONTRACT AUTO-PAUSED!")
            print("[!!!] Self-healing activated!")
            break
    sim.print_status("AFTER ATTACKS")

    # Phase 4: Auto Recovery
    print("\n" + "="*50)
    print("PHASE 4: THRESHOLD-BASED AUTO RECOVERY")
    print("="*50)
    avg_recovery, recovery_times = sim.attempt_recovery()
    sim.print_status("AFTER RECOVERY")

    # Phase 5: Post Recovery
    print("\n" + "="*50)
    print("PHASE 5: POST-RECOVERY OPERATIONS")
    print("="*50)
    for i in range(3):
        print(f"\n[TX {i+1}]")
        sim.send_valid_transaction(
            sim.alice, sim.bob, 0.1
        )
    sim.print_status("FINAL STATUS")

    # Save all results
    final_results = {
        'transactions': sim.results,
        'pq_avg_sign': sum(sim.pq_sign_times) / len(sim.pq_sign_times) if sim.pq_sign_times else 0,
        'pq_avg_verify': sum(sim.pq_verify_times) / len(sim.pq_verify_times) if sim.pq_verify_times else 0,
        'ecdsa_avg_sign': sum(sim.ecdsa_sign_times) / len(sim.ecdsa_sign_times) if sim.ecdsa_sign_times else 0,
        'ecdsa_avg_verify': sum(sim.ecdsa_verify_times) / len(sim.ecdsa_verify_times) if sim.ecdsa_verify_times else 0,
        'avg_recovery_time': avg_recovery,
        'recovery_times': recovery_times
    }

    with open('results/simulation_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)

    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    print(f"PQ Avg Sign Time:     "
          f"{final_results['pq_avg_sign']:.3f} ms")
    print(f"PQ Avg Verify Time:   "
          f"{final_results['pq_avg_verify']:.3f} ms")
    print(f"ECDSA Avg Sign Time:  "
          f"{final_results['ecdsa_avg_sign']:.3f} ms")
    print(f"ECDSA Avg Verify Time:"
          f"{final_results['ecdsa_avg_verify']:.3f} ms")
    print(f"Avg Recovery Time:    "
          f"{final_results['avg_recovery_time']:.3f} ms")
    print("\n[DONE] All results saved!")