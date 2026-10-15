import base64
import time

def print_header():
    print("=" * 50)
    print("      TERMINAL HACKER TOOLKIT     ")
    print("=" * 50)

def encode_base64():
    text = input("\n[+]Enter text to encode: ")
    encoded = base64.b64encode(text.encode()).decode()
    print(f"[>] Encoded (Text): {encoded}\n")

def decode_base64():
    text = input("\n[+] Enter base64 String to decode: ")
    try:
        decoded = base64.b64decode(text.encode()).decode()
        print(f"[>] Decoded (text): {decoded}\n")
    except Exception as e:
        print(f"[!] Invalid Base64 String! Error {e}\n")

def main():
    while True:
        print_header()
        print("1. Encode Text to Base64")
        print("2. Decode Base64 String")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ")

        if choice == "1":
            encode_base64()
        elif choice == "2":
            decode_base64()
        elif choice == "3":
            print("[+] Exiting Toolkit. Enjoy!!!")
            break
        else:
            print("[!] Invalid option, try again.\n")

if __name__ == "__main__":
    main()