
import os
from Crypto.Cipher import AES

def read_bmp(data):
  with open(data, "rb") as f:
    image = f.read()
  return image

def write_bmp(filepath, data):
  with open(filepath, "wb") as f:
    image = f.write(data)
  return image

def random_key(length=16):
  return os.urandom(length)

def random_iv(length=16):
  return os.urandom(length)

def xor(previous, next):
  result = bytearray(len(previous))
  for i in range(len(previous)):
    result[i] = previous[i] ^ next[i]
  return bytes(result)

def padding_PKCS7(data, block_size = 16):
  length_pad = block_size - (len(data) % block_size)
  padding = bytes([length_pad]* length_pad)
  return data + padding

def ecb(image_data, random_key):
  cipher = AES.new(random_key, AES.MODE_ECB)
  padding_data = padding_PKCS7(image_data, AES.block_size)
  ciphertext = b""

  for i in range(0, len(padding_data), AES.block_size):
    block = padding_data[i:i + AES.block_size]
    encrypted = cipher.encrypt(block)
    ciphertext += encrypted
  return ciphertext

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

def main():
  input = "/content/mustang.bmp"
  if not os.path.exists(input):
        print(f"File not found: {input}")
        return
  data = read_bmp(input)
  header = data[:54]
  image = data[54:]

  key = random_key()
  iv = random_iv()

  generated_ecb_ciphertext = ecb(image, key)
  output_ecb = "/content/mustang-ecb.bmp"
  write_bmp(output_ecb, header + generated_ecb_ciphertext)
  print(f"Wrote CBC to {output_ecb}")
  generated_cbc_ciphertext = cbc(image, key, iv)
  output_cbc = "/content/mustang-cbc.bmp"
  write_bmp(output_cbc, header + generated_cbc_ciphertext)
  print(f"Wrote CBC to {output_cbc}")

if __name__ == "__main__":
    main()