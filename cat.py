import argparse
import os

# To accept commands in CMD like script.py -h
working_dir = os.getcwd()


parser = argparse.ArgumentParser(description="Demo CLI")
parser.add_argument("filename", help="File to read")
parser.add_argument("-n", "--number", action="store_true", help="Show line numbers")

args = parser.parse_args()

file_name = args.filename

print("Filename:", args.filename)
if args.number:
    print("Option -n was used")

print(f"working in DIR: {working_dir}")
print()

# file_name = input("[>] Enter file name: ")

with open(f"{working_dir}\\{file_name}", 'r') as f:
	data = f.readlines()

for line in data:
	print(line)