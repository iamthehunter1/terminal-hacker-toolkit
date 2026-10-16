import base64
import hashlib
import math
import time
import os
import re
import secrets
import string
import sys
import urllib.parse


# pe headers

try:
    import pefile
    PEFILE_AVAILABLE = True
except ImportError:
    PEFILE_AVAILABLE = False

try:
    from capstone import CS_ARCH_X86, CS_MODE_32, CS_MODE_64, Cs
    CAPSTONE_AVAILABLE = True
except ImportError:
    CAPSTONE_AVAILABLE = False



# ascii banner

def print_banner():
    print("\n" + "=" * 65)
    print(r"""
  ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
  ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
        [+] TERMINAL HACKER TOOLKIT  [+]
        [+]    Created by Hunter     [+]
    """)
    print("=" * 65)


#encoder & decoder

def encode_base64():
    text = input("\n[+] Enter text to encode: ")
    encoded = base64.b64encode(text.encode()).decode()
    print(f"[>] Encoded (Text): {encoded}\n")

def decode_base64():
    text = input("\n[+] Enter Base64 string to decode: ")
    try:
        decoded = base64.b64decode(text.encode()).decode()
        print(f"[>] Decoded (text): {decoded}\n")
    except Exception as e:
        print(f"[!] Invalid Base64 String! Error {e}\n")

def base64_menu():
    while True:
        print("\n--- Base64 Encoder / Decoder ---")
        print("1. Encode Text to Base64")
        print("2. Decode Base64 String")
        print("3. Back to Main Menu")
        
        choice = input("\nSelect option (1-3): ")
        if choice == "1":
            encode_base64()
        elif choice == "2":
            decode_base64()
        elif choice == "3":
            break
        else:
            print("[!] Invalid option, try again.")

def text_to_hex():
    text = input("\n[+] Enter text to convert to Hex: ")
    print(f"[>] Hex String: {text.encode().hex()}\n")

def hex_to_text():
    hex_str = input("\n[+] Enter Hex to decode : ")
    try:
        decoded = bytes.fromhex(hex_str).decode("utf-8", errors="replace")
        print(f"[>] Decoded Text: {decoded}\n") 
    except Exception as e:
        print(f"[!] Hex Decoding error: {e}\n")

def hex_menu():
    while True:
        print("\n--- Hex Converter ---")
        print("1. Text -> Hex")
        print("2. Hex -> Text")
        print("3. Back to Main Menu")
        choice = input("\nSelect an option (1-3): ").strip()
        if choice == "1":
            text_to_hex()
        elif choice == "2":
            hex_to_text()
        elif choice == "3":
            break
        else:
            print("[!] Invalid option, try again")

def url_menu():
    while True:
        print("\n--- URL Encoder / Decoder ---")
        print("1. URL Encode Text")
        print("2. Url Decode String")
        print("3. Back to Main Menu")
        choice = input("\nSelect an option (1-3): ").strip()
        if choice == "1":
            text = input("\n[+] Enter String to URL Encode: ")
            print(f"[>] Encoded: {urllib.parse.quote(text)}\n")
        elif choice == "2":
            text = input("\n[+] Enter URL Encoded String: ")
            print(f"[>] Decoded: {urllib.parse.unquote(text)}\n")
        elif choice == "3":
            break
        else:
            print("[!] Invalid option, try again.")

#hashes


def generate_hashes():
    text = input("\n[+] Enter text to hash: ")
    print("\n[>] Generated Hashes:")
    print(f"    MD5:    {hashlib.md5(text.encode()).hexdigest()}")  
    print(f"    SHA1:   {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"    SHA256: {hashlib.sha256(text.encode()).hexdigest()}\n")

def generate_token():
    print("\n--- Secure Password Generator ---")
    length = input("[+] Enter Desired length (default 16): ").strip()
    length = int(length) if length.isdigit() and int(length) > 0 else 16
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    token = ''.join(secrets.choice(alphabet) for _ in range(length)) 
    print(f"[>] Generated Key: {token}/n")

def main():
    while True:
        print_banner()
        print("1. Base64 Encoder / Decoder")
        print("2. Hash Generator (MD5, SHA1, SHA256)")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ")

        if choice == "1":
            base64_menu()
        elif choice == "2":
            generate_hashes()
        elif choice == "3":  
            print("\n[+] Exiting toolkit. Enjoy!!!")
            break
        else:
            print("\n[!] Invalid Option, try again.\n")

if __name__ == "__main__":
    main()    
