# scripts/pq_sign.py
# Post-Quantum Signing using ML-DSA-65 (Dilithium3)

import oqs
import time
import warnings
warnings.filterwarnings('ignore')

class PostQuantumSigner:
    def __init__(self):
        self.algorithm = 'ML-DSA-65'
        self.sig = oqs.Signature(self.algorithm)
        self.public_key = None
        self.private_key = None
        
    def generate_keys(self):
        """Generate PQ keypair"""
        self.public_key = self.sig.generate_keypair()
        print(f"[PQ] Keys generated using {self.algorithm}")
        print(f"[PQ] Public key size: {len(self.public_key)} bytes")
        return self.public_key
    
    def sign_transaction(self, transaction_data):
        """Sign a transaction with PQ signature"""
        start_time = time.time()
        
        if isinstance(transaction_data, str):
            transaction_data = transaction_data.encode()
            
        signature = self.sig.sign(transaction_data)
        
        end_time = time.time()
        signing_time = (end_time - start_time) * 1000
        
        print(f"[PQ] Transaction signed in {signing_time:.4f} ms")
        print(f"[PQ] Signature size: {len(signature)} bytes")
        
        return signature, signing_time
    
    def verify_transaction(self, transaction_data, signature):
        """Verify a PQ signature"""
        start_time = time.time()
        
        if isinstance(transaction_data, str):
            transaction_data = transaction_data.encode()
        
        try:
            is_valid = self.sig.verify(
                transaction_data, 
                signature, 
                self.public_key
            )
        except Exception:
            is_valid = False
            
        end_time = time.time()
        verify_time = (end_time - start_time) * 1000
        
        status = "VALID" if is_valid else "INVALID"
        print(f"[PQ] Signature {status} - verified in {verify_time:.4f} ms")
        
        return is_valid, verify_time


if __name__ == "__main__":
    print("=" * 50)
    print("POST-QUANTUM SIGNATURE TEST")
    print("=" * 50)
    
    # Create signer
    pq_signer = PostQuantumSigner()
    pq_signer.generate_keys()
    
    # Test valid transaction
    print("\n--- Valid Transaction Test ---")
    tx = "Transfer 500 ETH from Alice to Bob"
    signature, sign_time = pq_signer.sign_transaction(tx)
    is_valid, verify_time = pq_signer.verify_transaction(tx, signature)
    
    # Test invalid transaction (attack simulation)
    print("\n--- Attack Simulation (Tampered Transaction) ---")
    fake_tx = "Transfer 500 ETH from Alice to ATTACKER"
    is_valid, verify_time = pq_signer.verify_transaction(
        fake_tx, signature
    )
    
    print("\n[PQ] Test Complete")