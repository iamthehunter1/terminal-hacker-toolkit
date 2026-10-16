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


# reverse engineering and malware analysis

def analyze_file():
    filepath = input("\n[+] Enter Path to target binary/file: ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: file path does not exist!/n")
        return

    file_size = os.path.getsize(filepath)
    print(f"\n[>] Target file: {os.path.basename(filepath)}")
    print(f"   Full Path: {filepath}")
    print(f"    Size:      {file_size} bytes ({round(file_size / 1024, 2)} KB)")

    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
            sha256_hash.update(byte_block)

    print(f"    MD5:      {md5_hash.hexdigest()}")
    print(f"    SHA256    {sha256_hash.hexdigest()}\n")    

def hex_dump():
    filepath = input("\n[+] Enter path to target file: ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: File does not exist!\n")
        return

    limit = input("[+] Number of bytes to dump (default 256): ").strip()
    limit = int(limit) if limit.isdigit() else 256

    print(f"\n[+] Hex Dump (First {limit} bytes):\n")
    with open(filepath, "rb") as f:
        chunk = f.read(limit)
        for i in range(0, len(chunk), 16):
            sub_chunk = chunk[i:i+16]
            hex_str = ' '.join(f'{b:02X}' for b in sub_chunk)
            ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in sub_chunk)
            print(f"{i:08X}  {hex_str:<48}  |{ascii_str}|")
    print()

def check_entropy():
    filepath = input("\n[+] Enter Path to target binary: ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: File path does not exist!\n")
        return

    with open(filepath, "rb") as f:
        data = f.read()

    if not data:
        print("[-] file is empty!\n")
        return

    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)

    entropy = round(entropy, 4)
    print(f"\n[+] Shanon Entropy: {entropy} / 8.0")
    if entropy > 7.0:
        print("[!] ALERT: High entropy detected! File is likely PACKED, COMPRESSED, or ENCRYPTED.")
    elif entropy < 1.0:
        print("[!] NOTE: Extremely low entropy. File mostly contains repetitive bytes or zeros.")
    else:
        print("[+] Normal Entropy: Standard Binary or text data.\n")


def extract_strings():
    filepath = input("\n[+] Enter path to target binary: ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: File does not exist!\n")
        return

    min_len = 4
    print(f"\n[+] Extracting printable ASCII strings (Min length {min_len})...\n")
    
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    
    found_ips = set()
    found_urls = set()

    with open(filepath, "rb") as f:
        data = f.read()
        current = ""
        for byte in data:
            if 32 <= byte <= 126:
                current += chr(byte)
            else:
                if len(current) >= min_len:
                    if ip_pattern.findall(current):
                        found_ips.update(ip_pattern.findall(current))
                    if url_pattern.findall(current):
                        found_urls.update(url_pattern.findall(current))
                current = ""

    if found_urls:
        print("[>] Potential URLs Found:")
        for url in found_urls:
            print(f"    - {url}")
    if found_ips:
        print("[>] Potential IP Addresses Found:")
        for ip_address in found_ips:  # Fixed variable name here
            print(f"    - {ip_address}")

    print("\n[+] Extraction complete!\n")

def parse_pe_headers():
    if not PEFILE_AVAILABLE:
        print("\n[!] 'pefile' module is not installed! Run: pip install pefile\n")
        return

    filepath = input("\n[+] Enter path to windows Pe binary (.exe/dll): ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: file does not exist!\n")
        return

    try:
        pe = pefile.PE(filepath)
        print("\n[>] PE Header Analysis:")
        print(f"    Entry Point (RVA): 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08X}")
        print(f"    Image Base:        0x{pe.OPTIONAL_HEADER.ImageBase:08X}")
        print(f"    Number of Sections: {pe.FILE_HEADER.NumberOfSections}")

        print("\n[>] PE Sections: ")
        for section in pe.sections:
            sec_name = section.Name.decode('utf-8', errors='ignore').rstrip("\x00")
            print(f"    - {sec_name:<10} VirtSize: 0x{section.Misc_VirtualSize:08X}  RawSize: 0x{section.SizeOfRawData:08X}  Entropy: {round(section.get_entropy(), 2)}")

        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            print("\n[>] Imported DLLs: ")
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8', errors='ignore')
                print(f"     -{dll_name} ({len(entry.imports)} imports)")
            print()
    except Exception as e:
        print(f"[!] PE Parsing Error: {e}\n")

def disassemble_bytes():
    if not CAPSTONE_AVAILABLE:
        print("\n[!] 'capstone' module is not installed! run: pip install capstone\n")
        return

    hex_bytes = input("\n[+] Enter hex bytes to dissamble (e.g. 55488b05b8130000): ").strip()
    try:
        code = bytes.fromhex(hex_bytes)
    except ValueError:
        print("[-] Invalid Hex Strings!\n")
        return

    arch = input("[+] Select Architecture (32/64) [default 64]: ").strip()
    mode = CS_MODE_32 if arch == "32" else CS_MODE_64

    md = Cs(CS_ARCH_X86, mode)
    print(f"\n[>] Disassembly Output ({'x86_32' if arch == '32' else 'x86_64'}):")
    for insn in md.disasm(code, 0x1000):
        print(f"   0x{insn.address:x}\t{insn.mnemonic}\t{insn.op_str}")
    print()


# sub menu

def re_toolkit_menu():
    while True:
        print("\n--- Reverse Engineering & Binary Analysis ---")
        print("1. File Metadata & hash analyzer ")
        print("2. Calculate shannon entropy (packet detection) ")
        print("3. Hex dump Binary bytes")
        print("4. Extract IOC Strings (URLs, IPs)")
        print("5. Parse Windows PE Headers (requires pefile)")
        print("6. Disassemble Hex Machine code (requires capstone)")
        print("7. Back to Main Menu")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            analyze_file()
        elif choice == "2":
            check_entropy()
        elif choice == "3":
            hex_dump()
        elif choice == "4":
            extract_strings()
        elif choice == "5":
            parse_pe_headers()
        elif choice == "6":
            disassemble_bytes()
        elif choice == "7":
            break
        else:
            print("[!] Invalid selection, try again!")

# main menu

def main():
    while True:
        print_banner()
        print(" 1. Base64 Encoder / Decoder")
        print(" 2. Hex Converter (Text <-> Hex)")
        print(" 3. URL Encoder / Decoder")
        print(" 4. Hash Generator (MD5, SHA1, SHA256)")
        print(" 5. Secure Password / Key Generator")
        print(" 6. Reverse Engineering & Binary Analysis Toolkit")
        print(" 7. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":    
            base64_menu()
        elif choice == "2":
            hex_menu()
        elif choice == "3":
            url_menu()
        elif choice == "4":
            generate_hashes()
        elif choice == "5":
            generate_token()
        elif choice == "6":       
            re_toolkit_menu()
        elif choice == "7":
            print("\n[+] Exiting toolkit. Keep grinding!")
            break
        else:
            print("\n[!] Invalid Option, try again.\n")

if __name__ == "__main__":
    main()