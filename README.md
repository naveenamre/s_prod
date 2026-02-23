# 🚀 SuperVibe Engine V2.0

Welcome to **SuperVibe Engine V2.0**! This is a custom, local, Python-based pipeline designed to intelligently auto-inject study syllabuses (or any bulk tasks) into the **Super Productivity** app.

Instead of manually typing out 50+ lectures, this engine reads a simple JSON syllabus, assigns Energy Tags (High/Medium/Low), applies duplicate protection, and generates a safe, import-ready backup file—all without touching or destroying your existing data. It's the ultimate "No Bakchodi" setup. 😎

---

## ✨ Key Features

* **🛡️ The Duplicate Shield:** Idempotent injection. If you accidentally drop the same syllabus twice, the engine smartly checks the `backlogTaskIds` and `taskIds` and skips existing tasks. No cloning!
* **⚡ Energy-Based Auto-Tagging:** Automatically creates and assigns color-coded tags (`High Energy`, `Medium Energy`, `Low Energy`) based on the input JSON.
* **🎩 The Illusionist (Safe Backup Modification):** Reads your fresh `base-backup.json`, safely injects new project data into the `data` or `state` tree, and packages it perfectly into `vibe-ready.json`.
* **👁️ Zero-Friction Watchman:** A continuously running background script (`file_watcher.py`) that monitors the `inputs` folder and processes files the moment they are dropped.

---

## 📂 Directory Structure

Make sure your setup matches this exact hierarchy for the engine to work seamlessly:

```text
SuperVibe_Engine/
│
├── 📁 data/                        
│   ├── 📁 inputs/                  # 👈 Drop your new syllabus JSONs here
│   └── 📁 processed/               # 🧹 Successfully injected JSONs are moved here
│
├── 📁 src/                         
│   ├── 📁 core/
│   │   ├── sp_injector.py          # The Brain: Modifies the backup JSON safely
│   │   ├── sp_models.py            # Super Productivity UUIDs and schema formats
│   │   └── file_watcher.py         # The Watchman: 24/7 background folder monitoring
│   │
│   └── 📁 utils/
│       ├── time_calc.py            # Duration/time converters
│       └── logger.py               # Terminal status visuals
│
├── 📄 base-backup.json             # ⚠️ YOUR FRESH EXPORT FROM THE APP GOES HERE
├── 📄 vibe-ready.json              # 🟢 THE ENGINE'S OUTPUT (Import this to the app)
├── 📄 super_vibe_config.json       # Custom color and theme settings
├── 📄 main_engine.py               # Main trigger file
└── 🚀 start_engine.bat             # Windows executable shortcut to start the Watchman

```

---

## 🏃‍♂️ Standard Operating Procedure (SOP)

Follow this strict 4-step "Import/Export" flow to ensure zero data loss and perfect sync (especially if you are using Dropbox/Google Drive for cloud syncing):

**Step 1: Get the Fresh Baseline (Export)**
Open your Super Productivity App. Go to **Settings (⚙️) -> Sync & Backup -> Export Data**.
Save the downloaded file directly into your `SuperVibe_Engine/` root folder and rename it exactly to **`base-backup.json`**.

**Step 2: Start the Engine**
Double-click `start_engine.bat`. You should see the terminal pop up:
`👀 SUPER-VIBE WATCHER V2.0 IS ACTIVE (MANUAL IMPORT MODE)`

**Step 3: Drop the Payload**
Drag and drop your syllabus JSON file (e.g., `chemistry.json` or `japanese.json`) into the `SuperVibe_Engine/data/inputs/` folder.
The terminal will process it instantly, print `"✅ SUCCESS! Created 'vibe-ready.json'"`, and move your input file to the `processed/` folder.

**Step 4: The Magic Manifestation (Import)**
Go back to your Super Productivity App. Navigate to **Settings (⚙️) -> Sync & Backup -> Import from File**.
Select the newly generated **`vibe-ready.json`** located in your root folder. Your new project will instantly appear in the sidebar with all tasks sitting cleanly in the Backlog!

---

## 📝 Input JSON Blueprint

To ensure the engine parses your data correctly, format your syllabus files like this:

```json
{
  "project_name": "Chemistry Semester Preparation",
  "tasks": [
    {
      "name": "Unit 1 - Rutherford Model",
      "duration": 1, 
      "energy_req": "High",
      "notes": "Focus on alpha particle scattering experiment."
    },
    {
      "name": "Unit 2 - Thermodynamics Basics",
      "duration": 1.5,
      "energy_req": "Medium",
      "notes": "Revise the zeroth and first laws."
    }
  ]
}

```

*(Note: `duration` is multiplied by 60 mins and converted to milliseconds automatically by the engine)*.