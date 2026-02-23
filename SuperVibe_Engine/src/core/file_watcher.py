import os
import sys
import time
import json
import shutil
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)

INPUTS_DIR = os.path.join(BASE_DIR, "data", "inputs")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
# SYNC_FILE yahan hum reference ke liye de rahe hain, injector iske folder mein base-backup dhoondhega
SYNC_FILE = os.path.join(BASE_DIR, "dummy.json") 

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core.sp_injector import inject_syllabus

for d in [INPUTS_DIR, PROCESSED_DIR]:
    os.makedirs(d, exist_ok=True)

def process_new_files():
    files = [f for f in os.listdir(INPUTS_DIR) if f.endswith(".json")]
    if not files:
        return False

    print(f"\n📂 [{datetime.now().strftime('%H:%M:%S')}] Watchman ne {len(files)} nayi file(s) pakdi! Process shuru...")
    
    for filename in files:
        filepath = os.path.join(INPUTS_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                syllabus_data = json.load(f)
            
            # Injector call
            success = inject_syllabus(syllabus_data, SYNC_FILE)

            if success:
                shutil.move(filepath, os.path.join(PROCESSED_DIR, filename))
                print(f"   🧹 Safayi done: '{filename}' processed folder mein shift ho gayi.")

        except Exception as e:
            print(f"   ❌ Error in '{filename}': {e}")

    print("🔥 SAB DONE! Engine waiting for next input...\n")
    return True

def start_watching():
    print("==================================================")
    print("👀 SUPER-VIBE WATCHER V2.0 IS ACTIVE (MANUAL IMPORT MODE)")
    print(f"   - Inputs: {INPUTS_DIR}")
    print("   Drop JSON files... Press Ctrl+C to stop.")
    print("==================================================")
    
    try:
        while True:
            process_new_files()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n💤 Watchman so gaya. Engine Shutdown.")

if __name__ == "__main__":
    start_watching()