import base64
import hashlib
import time

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

def generate_hashes():
    text = input("\n[+] Enter text to hash: ")
    print("\n[>] Generated Hashes:")
    print(f"    MD5:    {hashlib.md5(text.encode()).hexdigest()}")  
    print(f"    SHA1:   {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"    SHA256: {hashlib.sha256(text.encode()).hexdigest()}\n")

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