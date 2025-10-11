# Made completely by T3CHN0

# Get all needed libraries ready
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def red_text(text):return f"\033[1;31m{text}\033[0m"
def green_text(text):return f"\033[1;32m{text}\033[0m"
def blue_text(text):return f"\033[1;34m{text}\033[0m"
def magenta_text(text):return f"\033[0;35m{text}\033[0m"
def cyan_text(text):return f"\033[0;36m{text}\033[0m"
def bright_yellow_text(text):return f"\033[1;33m{text}\033[0m"

print(cyan_text("### Made By T3CHN0_707          ###"))
print(cyan_text("### simple tool used to decrypt ###"))
print(cyan_text("### data using AES encryption   ###"))
print()
print(magenta_text("--------------------------------------"))
print()


"""
The salt makes each password hash
unique even if passwords are the same
it makes it more powerful instead of
using just the password
"""
salt = b'\xee\xb1\x98\xb1e\xd3\xbb\xffOaG{a4F\xcc$\x84\x89I\xbd:\x99\x08\xd4K\x8eF\x8c\xcdV)'
# enryption password
password = "technoisnowgniyalp"

# generate new powerful key
# with the salt
# this key is unchangeable
# this key is important don't show
# to any one
key = PBKDF2(
	password=password,
	salt=salt, dkLen=32)

# decrypt data from the
# key file with read binary mode
with open("key.ttk", "rb") as keyF:
	iv = keyF.read(16)
	decrypt_data = keyF.read()

decrypting_cipher = AES.new(key, AES.MODE_CBC, iv)
original = unpad(decrypting_cipher.decrypt(decrypt_data), AES.block_size)
print(green_text(f"[+] Original Data: {original.decode()}"))
print()
print(magenta_text("--------------------------------------"))
print()
input(blue_text("Press Enter To Exit"))