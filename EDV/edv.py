# Made completely by T3CHN0

# Get all needed libraries ready
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from colorama import init, Fore, Style
import sys

init(autoreset=True)

def red_text(text): return Fore.RED + f"{text}" + Style.RESET_ALL
def green_text(text): return Fore.GREEN + f"{text}" + Style.RESET_ALL
def blue_text(text): return Fore.BLUE + f"{text}" + Style.RESET_ALL
def magenta_text(text): return Fore.MAGENTA + f"{text}" + Style.RESET_ALL
def cyan_text(text): return Fore.CYAN + f"{text}" + Style.RESET_ALL
def bright_yellow_text(text): return Style.BRIGHT + Fore.YELLOW + f"{text}" + Style.RESET_ALL

INpass = input(red_text("[>] Enter the password of this tool:\n"))
if INpass == "hardplay":
	print(green_text("[!] VALID PASSWORD"))
else:
	print(red_text("[!] WRONG PASSWORD DON'T TRY AGAIN IF YOU DON'T OWN THE TOOL"))
	sys.exit()

print()
print(cyan_text("### Made By T3CHN0_707          ###"))
print(cyan_text("### simple tool used to encrypt ###"))
print(cyan_text("### data using AES encryption   ###"))
print(magenta_text("--------------------------------------"))
print(bright_yellow_text("1. Encrypt"))
print(bright_yellow_text("2. Decrypt"))
print()
option = int(input(blue_text("[>] Enter the option number: ")))
print()
print(magenta_text("--------------------------------------"))

def encrypt():
	filetoencrypt = input(blue_text("[>] Enter file name without the extention:\n"))
	with open(f"{filetoencrypt}.ttk", "rb") as f:
		data = f.read()

	enfilename = input(blue_text("[>] Enter new file name to encrypted data in without the extention:\n"))
	salt = b'\xee\xb1\x98\xb1e\xd3\xbb\xffOaG{a4F\xcc$\x84\x89I\xbd:\x99\x08\xd4K\x8eF\x8c\xcdV)'
	password = "technoisnowgniyalp"
	key = PBKDF2(
		password=password,
		salt=salt, dkLen=32)
	cipher = AES.new(key, AES.MODE_CBC)
	# msg_data = bytes(
	# 	data,
	# 	encoding='utf-8')
	msg_data = data
	ciphered_data = cipher.encrypt(pad(msg_data, AES.block_size))
	with open(f"{enfilename}.ttk", "wb") as keyF:
		keyF.write(cipher.iv)
		keyF.write(ciphered_data)




def decrypt():
	filename = input(blue_text("[>] Enter file name (without the .ttk): "))
	defilename = input(blue_text("[>] Enter the output file name (without the extention): "))
	salt = b'\xee\xb1\x98\xb1e\xd3\xbb\xffOaG{a4F\xcc$\x84\x89I\xbd:\x99\x08\xd4K\x8eF\x8c\xcdV)'
	password = "technoisnowgniyalp"
	key = PBKDF2(
		password=password,
		salt=salt, dkLen=32)
	with open(f"{filename}.ttk", "rb") as keyF:
		iv = keyF.read(16)
		decrypt_data = keyF.read()

	decrypting_cipher = AES.new(key, AES.MODE_CBC, iv)
	original = unpad(decrypting_cipher.decrypt(decrypt_data), AES.block_size)
	with open(f"{defilename}.ttk", "wb") as f:
		f.write(original)


if option == 1:
	encrypt()
elif option == 2:
	decrypt()
else:
	print(red_text("[!] Invalid Input"))
	sys.exit()

print(green_text("[+] Mission Is Completed"))