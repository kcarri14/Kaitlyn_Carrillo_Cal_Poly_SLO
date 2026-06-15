import os
import random
import hashlib
from Crypto.Cipher import AES
import secrets
import time

def random_iv(length=16):
  return os.urandom(length)


def public_key(q,g):
  XA = secrets.randbelow(q - 1) + 1
  XB = secrets.randbelow(q - 1) + 1
  YA = pow(g, XA, q)
  YB = pow(g, XB, q)
  sA = pow(YB, XA, q)
  sB = pow(YA, XB, q)
  return YA,YB,sB, sA, XA,XB

def SHA256(sB,sA):
  sA_bytes = sA.to_bytes((sA.bit_length() + 7) // 8, 'big')
  sB_bytes = sB.to_bytes((sB.bit_length() + 7) // 8, 'big')
  sha256_hash_A = hashlib.sha256(sA_bytes).digest()
  kA = sha256_hash_A[:16]
  sha256_hash_B = hashlib.sha256(sB_bytes).digest()
  kB = sha256_hash_B[:16]
  return kA, kB

def compare_keys(kA,kB):
  t = "True"
  f = "False"
  if kA == kB:
    return t
  else:
    return f

def xor(previous, next):
  result = bytearray(len(previous))
  for i in range(len(previous)):
    result[i] = previous[i] ^ next[i]
  return bytes(result)

def padding_PKCS7(data, block_size = 16):
  length_pad = block_size - (len(data) % block_size)
  padding = bytes([length_pad]* length_pad)
  return data + padding

def cbc(image_data, random_key, random_iv):
  cipher = AES.new(random_key, AES.MODE_ECB)
  padding_data = padding_PKCS7(image_data, AES.block_size)
  ciphertext = random_iv
  previous = random_iv

  for i in range(0, len(padding_data), AES.block_size):
    block = padding_data[i:i + AES.block_size]
    xor_input = xor(previous, block)
    encrypted = cipher.encrypt(xor_input)
    ciphertext += encrypted
    previous = encrypted  #chain the keys

  return ciphertext
def unpadding_PKCS7(data):
  pad_len = data[-1]
  return data[:-pad_len]


def cbc_decrypt(ciphertext, random_key, random_iv):
    cipher = AES.new(random_key, AES.MODE_ECB)
    plaintext = b''
    previous = random_iv
    for i in range(16, len(ciphertext), AES.block_size):
        block = ciphertext[i:i + AES.block_size]
        decrypted = cipher.decrypt(block)
        xor_output = xor(decrypted, previous)
        plaintext += xor_output
        previous = block

    return unpadding_PKCS7(plaintext)

def main():
  q = "B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6 9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0 13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70 98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0 A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708 DF1FB2BC 2E4A4371"
  g = "A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213 160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1 909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24 855E6EEB 22B3B2E5"
  cleaned_q = q.replace(" ", "").replace("\n", "")
  cleaned_g = g.replace(" ", "").replace("\n", "")
  q1 = int(cleaned_q, 16)
  g1 = int(cleaned_g, 16)
  mA = "Hi Bob"
  mB = "Hi Alice"
  YA, YB, sB, sA,XA, XB = public_key(q1,g1)
  print(f"Alice's private key: {XA}\n")
  print(f"Alice's public key: {YA}\n")
  print(f"Bob's private key: {XB}\n")
  print(f"Bob's public key: {YB}\n")
  print(f"Alice's computed shared secret: {sA}\n")
  print(f"Bob's computed shared secret: {sB}\n")
  kA,kB = SHA256(sB,sA)
  print(f"Alice's dervied key: {kA.hex()}\n")
  print(f"Bob's dervied key: {kB.hex()}\n")
  results = compare_keys(kA, kB)
  print(f"Alice and Bob's keys are the same: {results}\n")
  iv_a = random_iv()
  cA = cbc(mA.encode(),kA,iv_a)
  print(f"Alice's message: {mA}\n")
  print(f"Alice's IV: {iv_a.hex()}\n")
  print(f"Alice's ciphertext: {cA[16:].hex()}\n")
  decrypted_cA = cbc_decrypt(cA,kB,iv_a).decode()
  print(f"Bob's decrypted message: {decrypted_cA}\n")
  iv_b = random_iv()
  cB = cbc(mB.encode(),kB,iv_b)
  print(f"Bob's message: {mB}\n")
  print(f"Bob's IV: {iv_b.hex()}\n")
  print(f"Bob's ciphertext: {cB[16:].hex()}\n")
  decrypted_cB = cbc_decrypt(cB,kA,iv_b).decode()
  print(f"Alice's decrypted message: {decrypted_cB}\n")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nRuntime: {time.time() - start:.4f} seconds")