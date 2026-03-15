import oqs
print('OQS version:', oqs.oqs_version())
sig = oqs.Signature('Dilithium3')
pub = sig.generate_keypair()
print('Dilithium3 working correctly')
