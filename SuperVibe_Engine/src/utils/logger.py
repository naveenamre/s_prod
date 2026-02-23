# src/utils/logger.py
from datetime import datetime

# ANSI Color Codes (Bina kisi external library (like colorama) ke colors print karne ka Jugad)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def _get_time():
    """Current time format karta hai"""
    return datetime.now().strftime('%H:%M:%S')

def info(msg: str):
    """Blue color mein Info"""
    print(f"{Colors.OKCYAN}ℹ️  [{_get_time()}] {msg}{Colors.ENDC}")

def success(msg: str):
    """Green color mein Success"""
    print(f"{Colors.OKGREEN}✅ [{_get_time()}] {msg}{Colors.ENDC}")

def warning(msg: str):
    """Yellow color mein Warning"""
    print(f"{Colors.WARNING}⚠️  [{_get_time()}] {msg}{Colors.ENDC}")

def error(msg: str):
    """Red color mein Error"""
    print(f"{Colors.FAIL}❌ [{_get_time()}] {msg}{Colors.ENDC}")

def step(msg: str):
    """Steps dikhane ke liye"""
    print(f"{Colors.OKBLUE}➡️  {msg}{Colors.ENDC}")

def title(msg: str):
    """Bada Title (Header)"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {msg} ==={Colors.ENDC}")

def divider():
    """Line draw karta hai"""
    print(f"{Colors.HEADER}--------------------------------------------------{Colors.ENDC}")