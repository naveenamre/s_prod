import os
import sys
import time

# --- 🗺️ SMART PATH SETUP ---
# Ye check karega ki file kahan hai, aur us hisaab se 'src' folder dhoondhega
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(CURRENT_DIR) != 'src':
    # Agar file bahar hai, toh usko 'src' folder ka rasta do
    sys.path.insert(0, os.path.join(CURRENT_DIR, 'src'))
else:
    # Agar file pehle se 'src' mein hai
    sys.path.insert(0, CURRENT_DIR)

# Ab hum apne banaye huye tools import kar sakte hain
from core.file_watcher import start_watching
from utils import logger

def print_banner():
    """Terminal pe Hacker wali vibe dene ke liye ASCII Art"""
    banner = """
     ██████╗ ██╗   ██╗██████╗ ███████╗██████╗        ██╗   ██╗██╗██████╗ ███████╗
    ██╔════╝ ██║   ██║██╔══██╗██╔════╝██╔══██╗       ██║   ██║██║██╔══██╗██╔════╝
    ███████╗ ██║   ██║██████╔╝█████╗  ██████╔╝       ██║   ██║██║██████╔╝█████╗  
    ╚════██║ ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗       ╚██╗ ██╔╝██║██╔══██╗██╔══╝  
    ███████║ ╚██████╔╝██║     ███████╗██║  ██║        ╚████╔╝ ██║██████╔╝███████╗
    ╚══════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝         ╚═══╝  ╚═╝╚═════╝ ╚══════╝
                        --- ENGINE V2.0 ---
    """
    print(f"{logger.Colors.HEADER}{logger.Colors.BOLD}{banner}{logger.Colors.ENDC}")

def main():
    # Windows/Mac ka terminal clear karna start hone se pehle
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    print_banner()
    logger.info("Initializing Super-Vibe Engine Components...")
    time.sleep(0.5)
    
    logger.step("Loading core modules (Injector, Models)...")
    time.sleep(0.3)
    logger.step("Connecting to Super Productivity JSON Database...")
    time.sleep(0.3)
    
    logger.success("All systems GO! 🚀")
    logger.divider()
    
    # 👁️ Watchman ko duty pe laga do
    try:
        start_watching()
    except Exception as e:
        logger.error(f"Engine Crash Ho Gaya Bhai: {e}")

if __name__ == '__main__':
    main()