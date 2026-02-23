import uuid
import time

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================
def generate_sp_id():
    """
    Super Productivity ka UUID format (21 chars long).
    Aise IDs banayega jo app ko bilkul native lagenge.
    """
    return str(uuid.uuid4()).replace('-', '')[:21]

def get_now_ms():
    """Current time in milliseconds (SP format)"""
    return int(time.time() * 1000)

# ==========================================
# 🏗️ ENTITY TEMPLATES (The Blueprints)
# ==========================================

def create_sp_project(title: str, theme_color: str = "#6495ED") -> dict:
    """Naya Project banane ka JSON blueprint"""
    project_id = generate_sp_id()
    return {
        "id": project_id,
        "title": title,
        "isHiddenFromMenu": False,
        "isArchived": False,
        "isEnableBacklog": True, # Always ON for Syllabus
        "backlogTaskIds": [],
        "taskIds": [],
        "noteIds": [],
        "icon": "library_books", # Project ke aage kitab ka icon aayega
        "theme": {
            "isAutoContrast": True,
            "isDisableBackgroundTint": False,
            "primary": theme_color,
            "huePrimary": "500",
            "accent": "#ff4081",
            "hueAccent": "500",
            "warn": "#e11826",
            "hueWarn": "500",
            "backgroundOverlayOpacity": 0
        }
    }

def create_sp_tag(title: str, color: str, icon: str = "bolt") -> dict:
    """Naya Tag (Level/Energy) banane ka JSON blueprint"""
    tag_id = generate_sp_id()
    now = get_now_ms()
    return {
        "id": tag_id,
        "title": title,
        "icon": icon,
        "color": color,
        "created": now,
        "modified": now,
        "taskIds": []
    }

def create_sp_task(title: str, duration_mins: int, project_id: str, tag_ids: list = None, notes: str = "") -> dict:
    """Naya Task (Lecture) banane ka JSON blueprint"""
    task_id = generate_sp_id()
    duration_ms = duration_mins * 60 * 1000 # Minutes to MS

    return {
        "id": task_id,
        "projectId": project_id,
        "subTaskIds": [],
        "timeSpentOnDay": {},
        "timeSpent": 0,
        "timeEstimate": duration_ms,
        "isDone": False,
        "doneOn": None,
        "title": title,
        "notes": notes,
        "tagIds": tag_ids or [],
        "parentId": None,
        "reminderId": None,
        "created": get_now_ms(),
        "repeatCfgId": None,
        "plannedAt": None,
        "dueDay": None,
        "attachments": [],
        "issueId": None,
        "issueProviderId": None
    }