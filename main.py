import base64
import hashlib
import math
import time
import os
import platform 
import shutil
from collections import Counter
from pathlib import Path
import re
import socket     
import secrets
import string
import sys
import json
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
    print(f"[>] Generated Key: {token}\n")


# reverse engineering and malware analysis


# TCP port scanner                   

def tcp_port_scanner():
    """ Scan selected TCP ports. """

    print("\n--- Tcp Port Scanner ---")            

    host = input("\n[+] Enter target hostname or IP: ").strip()      

    if not host:
        print("[-] Target cannot be Empty.\n")
        return      

    try:
        target_ip = socket.gethostbyname(host)
    except (socket.gaierror, UnicodeError):   
        print("[-] Could not resolve hostname or IP address\n")    
        return

    print(f"\n[+] Target: {host} ({target_ip})")       
    print("[+] Enter ports like 22,80,443 or a range like 100.")     
    port_input = input("[+] Ports to scan (default common ports: )").strip()        

    if not port_input:         
        ports = [
            21, 22, 23, 25, 53, 80, 110, 143,
            443, 445, 3306, 3389, 5432, 8080, 8443

        ]     
    else:
        try:
            ports = set()    

            for item in port_input.split(","):              
                item = item.strip()   

                if "-" in item:
                    parts = item.split("-")        

                    if len(parts) != 2:    
                        raise ValueError     

                    start_pot, end_port = map(int, parts)  

                    if start_pot > end_port:
                        raise ValueError   
                    

                    if end_port - start_pot > 9999:
                        print("[-] Max range size is 10,000 ports\n")
                        return        

                    ports.update(range(start_pot, end_port + 1))   
                else:
                    ports.add(int(item))    

            if not ports or any(p < 1 or p > 65535 for p in ports):  
                raise ValueError   

            ports = sorted(ports)

        except ValueError:
            print("[-] Invalid port input. Use ports from 1 to 65535\n")   
            return       

    print(f"\n Scanning {len(ports)} tcp ports\n")
    open_ports = []
                             
    for port in sorted(ports):     
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)   
                result = sock.connect_ex((target_ip, port))

                if result == 0:
                    open_ports.append(port)     
                    try: 
                        service = socket.getservbyport(port, "tcp")    
                    except OSError:
                        service = "unknown"

                    print(f"[OPEN]  Port {port:<5} Service: {service}")   

        except OSError:
            continue

    print("\n" + "=" * 40 )      
    print("TCP scan summary ")
    print("=" * 40) 
    print(f"Target:    {host} ({target_ip})")
    print(f"Ports tested:  {len(ports)} ")       
    print(f"Open ports:    {len(open_ports)}")    

    if open_ports:
        print("Open:      " + ", ".join(map(str, open_ports)))
    else:
        print("No open TCP ports detected ")

    print("\n[!] No open TCP ports detected ")  
    print("=" * 40 + "\n")


# log file analyzer    

def log_file_analyzer():
    """ Analyze a log file for errors, failed logins, and reported IP"""                

    print("\n--- Log File Analyzer ---")               
    file_path =  input("[+] Enter log file path: ").strip().strip('"')             


    path = Path(file_path)  

    if not path.is_file():          
        print("[-] File not found.\n")            
        return

    try:
        with path.open("r", encoding="utf-8", errors="replace") as file:         
            lines = file.readlines()
    except OSError as error:
        print(f"[-] Could not read file: {error}\n")
        return                      

    if not lines:
        print(f"[-] File is empty\n")
        return

    text = "".join(lines)      
    lower_text  = text.lower()            

    error_count = sum(
        1 for line in lines 
        if re.search(r"\b(error|critical|fatal)\b", line, re.I)            

    )   

    warning_count = sum(
        1 for line in lines
        if re.search(r"\b(warn|warning)\b", line, re.I)       
    )

    failed_login_count = sum(
        1 for line in lines   
        if re.search(
            r"failed login|login failed|authentication failed|"                          
            r"invalid password|invalid credentials",
            line,
            re.I        

        )
    )

    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"             
    ips = re.findall(ip_pattern, text)            

    valid_ips = [
        ip for ip in ips     
        if all(0 <= int(part) <= 255 for part in ip.split("."))                       
                      
    ]    

    ip_counts = Counter(valid_ips)                   

    print("\n" + '=' * 40)                       
    print("LOG ANALYSIS SUMMARY")    
    print("=" * 40)
    print(f"File:            {path.name}")          
    print(f"Total lines:     {len(lines)}") 
    print(f"Error lines:     {error_count}")                     
    print(f"Warning lines:   {warning_count}")              
    print(f"Failed logins:   {failed_login_count}")              

    print("\n--- Most Frequent IP Addresses ---")            

    if ip_counts:
        for ip, count in ip_counts.most_common(10):                              
            print(f"{ip:<18} {count} occurence(s)")      

    else:
        print("No valid IPv4 addresses found")  

    print("\n--- Failed login entries ---")   

    matching_lines = [
        (number, line.strip())
        for number, line in enumerate(lines, start=1)             
        if re.search(
            r"failed login|login failed|authentication failure|"   
            r"invalid password|invalid credentials",
            line,
            re.I    

        )

    ]

    if matching_lines:
        for number, line in matching_lines[:10]:
            print(f"Line {number}: {line[:200]}")   
        if len(matching_lines) > 10:
            print(f"...and {len(matching_lines) - 10} more.") 

    else:
        print("No matching failed-logins messages found")

    print("\n[!] Reported IPs or logs errors are indicators to check")
    print(" not proof of malicious activity")
    print("=" * 40 + "\n")

# system information


def system_information():
    """Display system details and check disk usage."""
    print("\n" + "=" * 45)
    print("     SYSTEM INFORMATION & DIAGNOSTICS")
    print("=" * 45)

    info = {
        "Hostname": socket.gethostname(),
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine(),
        "Processor": platform.processor() or "Not Available",
        "Python Version": platform.python_version(),
        "Current Directory": os.getcwd(),
    }

    print("\n[+] System Information\n")
    for label, value in info.items():
        print(f"    {label:<22}: {value}")

    print("\n[+] Disk Usage Check")
    directory = input(
        "\nEnter directory path to check (Enter for current directory): "
    ).strip().strip('"')

    if not directory:
        directory = os.getcwd()

    if not os.path.isdir(directory):
        print("[-] Error: Directory does not exist.\n")
        return

    try:
        disk = shutil.disk_usage(directory)
        total_gb = disk.total / (1024 ** 3)
        used_gb = disk.used / (1024 ** 3)
        free_gb = disk.free / (1024 ** 3)
        usage_percent = (disk.used / disk.total) * 100

        print(f"\n    Directory : {os.path.abspath(directory)}")
        print(f"    Total     : {total_gb:.2f} GB")
        print(f"    Used      : {used_gb:.2f} GB")
        print(f"    Free      : {free_gb:.2f} GB")
        print(f"    Usage     : {usage_percent:.1f}%")

        if usage_percent >= 90:
            print("\n[!] WARNING: Disk usage is critically high.")
        elif usage_percent >= 80:
            print("\n[!] Warning: Disk usage is high.")
        else:
            print("\n[+] Disk usage is within the configured warning limits.")

    except OSError as error:
        print(f"\n[-] Could not complete disk diagnostics: {error}\n")
        print("[+] System diagnostics complete.\n")
        return

    print("\n[+] System diagnostics complete.")

    save_report = input(
        "\nSave diagnostics report as JSON? (y/n): "
    ).strip().lower()

    if save_report != "y":
        print()
        return

    report = {
        **info,
        "Checked Directory": os.path.abspath(directory),
        "Disk Total GB": round(total_gb, 2),
        "Disk Used GB": round(used_gb, 2),
        "Disk Free GB": round(free_gb, 2),
        "Disk Usage Percent": round(usage_percent, 1),
    }

    report_path = input(
        "Enter report filename (default system_report.json): "
    ).strip().strip('"')

    if not report_path:
        report_path = "system_report.json"

    if not report_path.lower().endswith(".json"):
        report_path += ".json"

    try:
        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        print(f"\n[+] Report saved to: {os.path.abspath(report_path)}\n")

    except (OSError, ValueError) as error:
        print(f"\n[-] Could not save diagnostics report: {error}\n")

def analyze_file():
    filepath = input("\n[+] Enter Path to target binary/file: ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: file path does not exist!\n")                             
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

    print(f"   MD5:      {md5_hash.hexdigest()}")
    print(f"   SHA256    {sha256_hash.hexdigest()}\n")    


def calculate_sha256(filepath, chunk_size=1024 * 1024):
    """ Calculate a file's SHA-256 hash without loading it all into memory."""                              
    digest = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)

    return digest.hexdigest()

def file_integrity_check():
    """ Display a file's size and SHA-256 checksum."""   
    filepath = input("\n[+] Enter file path: ").strip().strip('"')

    if not os.path.isfile(filepath):
        print("[-] Error: File does not exist or is not a regular file.\n")
        return

    try:
        file_size = os.path.getsize(filepath)
        checksum = calculate_sha256(filepath)

        print("\n[+] File Integrity Report")
        print(f"    File:     {os.path.basename(filepath)}")
        print(f"    Size:     {file_size} bytes")
        print(f"    SHA256:   {checksum}")
        print("\n[+] Integrity  report compelete.\n")


    except (OSError, ValueError) as error:
        print(f"[-] Could not analyze file: {error}\n")

def compare_file_hashes():
    """Compare two files using their SHA-256 checksums. """
    first_path = input("\n[+] Enter path to first file: ").strip().strip('"')
    second_path = input("[+] Enter path to second file: ").strip().strip('"')

    for filepath in (first_path, second_path):
        if not os.path.isfile(filepath):                          
            print(f"[-] File does not exist or is not recognized: {filepath}\n")
            return

    try:
        first_hash = calculate_sha256(first_path)
        second_hash = calculate_sha256(second_path)

        print("\n[+] File Comparision")
        print(f"    file 1 SHA256: {first_hash}")
        print(f"    file 2 SHA256: {second_hash}")

        if first_hash == second_hash:
            print("[+] Result: Files have identical contents")
        else:
            print("[!] Result: Files have different contents")

        print()

    except (OSError, ValueError) as error:
        print(f"[-] Could not compare files: {error}\n") 

def detect_file_signature():
    """ Identify common file types using their magic bytes."""                

    signatures = [
        ("PE Signatures (EXE/DLL)", b"MZ", (".exe", ".dll", ".sys")),
        ("PNG Image", b"\x89PNG\r\n\x1a\n", (".png",)),
        ("JPEG Image", b"\xff\xd8\xff", (".jpg", ".jpeg")),
        ("PDF Document", b"%PDF-", (".pdf",)),
        ("ZIP archive", b"PK\x03\x04", (".zip",)),
        ("GIF Image", b"GIF8", (".gif",)),
    ]  

    filepath = input("\n[+] Enter file path: ").strip().strip('"')

    if not os.path.isfile(filepath):
        print("[-] Error: File does not exist or is not a regular file\n")
        return

    try:
        with open(filepath, "rb") as file:
            header = file.read(16)

        extension = os.path.splitext(filepath)[1].lower()

        print("\n[+] File Signature Report")
        print(f"   File:        {os.path.basename(filepath)}")
        print(f"   Extension:   {extension or '(none)'}")
        print(f"   Header:      {header.hex(' ').upper() or '(empty file)'}")

        detected = None
        for file_type, magic, valid_extensions in signatures:
            if header.startswith(magic):
                detected = (file_type, valid_extensions)
                break
 
        if detected:
            file_type, valid_extensions = detected
            print(f"    Detected: {file_type}")

            if extension not in valid_extensions:
                print("[!] Warning: Extensions does not match the detected format.")   
            else:
                print("[+] Extensions matches the detected format.")
        else:
            print("[?] Unknown file signature; no supported format matched. ")    

        print()
      
    except OSError as error:
        print(f"[-] Could not read file: {error}\n")

def yara_lite_scanner():
    """ Scan a file for known strings and byte patterns"""                           
    
    rules = [
        ("POWERSHELL", b"powershell", "Powershell reference", "LOW"),
        ("CMD_EXECUTION", b"cmd.exe", "Command interpreter reference", "LOW"),
        ("SCRIPT_HOST", b"wscript.exe", "Windows Script Host reference", "LOW"),
        ("REMOTE_THREAD", b"CreateRemoteThread",
         "Remote thread API reference", "MEDIUM"),
        ("MEMORY_WRITE", b"WriteProcessMemory",
         "Process memory-writing API reference", "MEDIUM"),
        ("MEMORY_ALLOC", b"VirtualAlloc",
         "Memory allocation API reference", "LOW"),
        ("URL_DOWNLOAD", b"URLDownloadToFile",
         "URL Download API reference ", "MEDIUM"),
        ("BASE64_DECODE", b"FromBase64String",
         "Base64 decoding reference", "LOW"),
        ("DEFENDER_CHANGE", b"DisableRealtimeMonitoring",
         "Possible Defender configuration reference", "HIGH"),
        ("RUN_KEY", b"CurrentVersion\\Run",
         "Possible Windows Run-key reference", "MEDIUM"),     

    ]

    filepath = input("\n[+] File path to scan: ").strip().strip('"')  

    if not os.path.isfile(filepath):
        print("[-] File does not exist or is not a regular file.\n")
        return

    custom = input (
        "[+] Optional custom ASCII string (Enter to skip):  "
                              
    ).strip()

    if custom:         
        rules.append((
            "CUSTOM_STRING",
            custom.encode("utf-8"),
            f"Custom indicator: {custom!r}",
            "INFO",
        ))

    findings = []
    chunk_size = 1024 * 1024  
    max_pattern_length = max(len(pattern) for _, pattern, _, _ in rules)
    overlap_size = max_pattern_length -1
    tail = b""
    total_read = 0

    try:
        with open(filepath, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                buffer = tail + chunk    
                base_offsets = total_read - len(tail)      
                lower_buffer = buffer.lower()     
                previous_tail_length  = len(tail)     
                total_read += len(chunk)    

                for name, pattern , description, severity in rules:    
                    needle = pattern.lower()    
                    start = 0 

                    while True:
                        position = lower_buffer.find(needle, start)       
                        if position == -1:
                            break     

                        if position + len(needle) > previous_tail_length:    
                            findings.append({
                                "name": name,
                                "offset": base_offsets + position,
                                "description": description,
                                "severity": severity,
                                "match": buffer[
                                    position:position + len(pattern)      
                                ],
                            })

                        start = position + 1      

                tail = buffer[-overlap_size:] if overlap_size else b""    

        findings.sort(key=lambda  finding: finding["offset"])

        save_report = input(
            "[+] Save scan report as JSON (y/n): "   
        ).strip().lower()

        if save_report == "y":
            report_path = input(
                "[+] Enter output filename "
                "(default scan_report.json): "

            ).strip().strip('"')

        if not report_path:
            report_path = "scan_report.json"

        report = {   
            "file": os.path.basename(filepath),
            "size_bytes": total_read,
            "rules_checked": len(rules),
            "total_matches": len(findings),
            "findings": [
                {
                    "name": finding["name"],
                    "offset": finding["offset"],
                    "severity": finding["severity"],
                    "description": finding["description"],
                    "match": finding["match"].decode(
                        "utf-8", errors="replace"
                    ),
                    "match_hex": finding["match"].hex(),
                }
                for finding in findings
                
            ],

        }    

        try:
            with open(
                report_path, "w", encoding="utf-8"       

            ) as report_file:
                json.dump(report, report_file, indent=4)

            print(f"[+] Report Saved to {report_path}")

        except OSError as error:
            print(f"[-] Could not save report: {error}")
          
        print("\n" + "=" * 60)         
        print("YARA-LITE  STATIC SCAN REPORT")    
        print("=" * 60)
        print(f"File: {os.path.basename(filepath)}")
        print(f"Size: {total_read:,} bytes")     
        print(f"Rules: {len(rules)}")           
        print(f"Matches: {len(findings)}\n")           

        if not findings:
            print("[+] No configured Indicators matched.  " )         
            print("[!] This does not prove the file is safe. ")          
        else:
            for finding in findings:
                print(
                    f"[{finding['severity']}] {finding['name']}\n"
                    f"     Offset: 0x{finding['offset']:X}\n"
                    f"     Detail: {finding['description']}\n"
                    f"     Match:  {finding['match']!r}\n"
                )                

            print("[!] Investigate matches in context; strings alone. ")
            print("    do not establish malicious behavior.   ")
                       
        print("=" * 60 + "\n")      

    except OSError as error:    
        print(f"[-] Scan failed: {error}\n")                        

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
        p_x = data.count(bytes([x])) / len(data)
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
    
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    url_pattern = re.compile(r"""https?://[^\s'"<>]+""", re.IGNORECASE)  
    
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

        if len(current) >= min_len:
            found_ips.update(ip_pattern.findall(current))
            found_urls.update(url_pattern.findall(current))

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
        print("\n[!] 'pefile' module is not installed! Run: pip install pefile.\n")
        return

    filepath = input("\n[+] Enter path to windows Pe binary (.exe/dll): ").strip()
    if not os.path.isfile(filepath):
        print("[-] Error: file does not exist.\n")
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
        print("7. File Integrity Check (SHA-256)")
        print("8. Compare Two files.")    
        print("9. File Signature detection.")   
        print("10. YARA-Lite Static Scanner")   
        print("11. TCP Port scanner")     
        print("12. Log File Analyzer")    
        print("13. System Information & Diagnostics")          
        print("14. Back to Main Menu.")      
         
   
        choice = input("\nSelect an option (1-14): ").strip()      

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
            file_integrity_check() 

        elif choice == "8":    
            compare_file_hashes() 

        elif choice =="9":      
            detect_file_signature()

        elif choice == "10":
            yara_lite_scanner() 

        elif choice == "11":
            tcp_port_scanner() 
                 
        elif choice == "12":
            log_file_analyzer()

        elif choice == "13":
            system_information()

        elif choice == "14":  
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
        print(" 6. Reverse Engineering & Binary Analysis Toolkit.")
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
