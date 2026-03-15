# scripts/ecdsa_sign.py
# Classical ECDSA Signing for comparison

from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import time
import hashlib

class ECDSASigner:
    def __init__(self):
        self.algorithm = 'ECDSA-SECP256k1'
        self.private_key = None
        self.public_key = None
        
    def generate_keys(self):
        """Generate ECDSA keypair"""
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        
        print(f"[ECDSA] Keys generated using {self.algorithm}")
        print(f"[ECDSA] Public key size: "
              f"{len(self.public_key.to_string())} bytes")
        return self.public_key
    
    def sign_transaction(self, transaction_data):
        """Sign transaction with ECDSA"""
        start_time = time.time()
        
        if isinstance(transaction_data, str):
            transaction_data = transaction_data.encode()
        
        tx_hash = hashlib.sha256(transaction_data).digest()
        signature = self.private_key.sign(tx_hash)
        
        end_time = time.time()
        signing_time = (end_time - start_time) * 1000
        
        print(f"[ECDSA] Transaction signed in {signing_time:.4f} ms")
        print(f"[ECDSA] Signature size: {len(signature)} bytes")
        
        return signature, signing_time
    
    def verify_transaction(self, transaction_data, signature):
        """Verify ECDSA signature"""
        start_time = time.time()
        
        if isinstance(transaction_data, str):
            transaction_data = transaction_data.encode()
        
        tx_hash = hashlib.sha256(transaction_data).digest()
        
        try:
            self.public_key.verify(signature, tx_hash)
            is_valid = True
        except BadSignatureError:
            is_valid = False
            
        end_time = time.time()
        verify_time = (end_time - start_time) * 1000
        
        status = "VALID" if is_valid else "INVALID"
        print(f"[ECDSA] Signature {status} - "
              f"verified in {verify_time:.4f} ms")
        
        return is_valid, verify_time


if __name__ == "__main__":
    print("=" * 50)
    print("ECDSA SIGNATURE TEST")
    print("=" * 50)
    
    signer = ECDSASigner()
    signer.generate_keys()
    
    print("\n--- Valid Transaction Test ---")
    tx = "Transfer 500 ETH from Alice to Bob"
    signature, sign_time = signer.sign_transaction(tx)
    is_valid, verify_time = signer.verify_transaction(tx, signature)
    
    print("\n--- Attack Simulation ---")
    fake_tx = "Transfer 500 ETH from Alice to ATTACKER"
    is_valid, verify_time = signer.verify_transaction(
        fake_tx, signature
    )