import json
import os
from core import sp_models

def load_config(base_dir):
    """Super Vibe Config ko load karta hai"""
    config_path = os.path.join(base_dir, "super_vibe_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def _get_or_create_tag(db, tag_name, color):
    if "tag" not in db: db["tag"] = {"ids": [], "entities": {}}
    tags = db["tag"]["entities"]
    
    for t_id, t_data in tags.items():
        if t_data.get("title", "").strip().lower() == tag_name.strip().lower():
            return t_id
            
    print(f"   🏷️ Creating Tag: '{tag_name}'")
    # ⚡ ENGINE LINK: Ab ye sp_models se blueprint uthayega
    new_tag = sp_models.create_sp_tag(tag_name, color)
    tag_id = new_tag["id"]
    db["tag"]["entities"][tag_id] = new_tag
    db["tag"]["ids"].append(tag_id)
    return tag_id

def _get_or_create_project(db, project_name, theme_color):
    if "project" not in db: db["project"] = {"ids": [], "entities": {}}
    projects = db["project"]["entities"]
    
    for p_id, p_data in projects.items():
        if p_data.get("title", "").strip().lower() == project_name.strip().lower():
            return p_id
            
    print(f"   🏗️ Creating Project: '{project_name}'")
    # ⚡ ENGINE LINK: sp_models ka project blueprint
    new_project = sp_models.create_sp_project(project_name, theme_color)
    proj_id = new_project["id"]
    db["project"]["entities"][proj_id] = new_project
    db["project"]["ids"].append(proj_id)
    
    if "menuTree" not in db: db["menuTree"] = {"projectTree": [], "tagTree": []}
    if "projectTree" not in db["menuTree"]: db["menuTree"]["projectTree"] = []
    db["menuTree"]["projectTree"].append({"k": "p", "id": proj_id})
    return proj_id

def inject_syllabus(syllabus_data, sync_file_path):
    print(f"\n💉 Reading base-backup.json for: {syllabus_data.get('project_name', 'Unknown')}")
    
    root_dir = os.path.dirname(sync_file_path)
    base_backup_path = os.path.join(root_dir, "base-backup.json")
    out_backup_path = os.path.join(root_dir, "vibe-ready.json")
    
    # ⚡ DYNAMIC CONFIG LOAD
    config = load_config(root_dir)
    tag_colors = config.get("tag_colors", {"High Energy": "#e11826", "Medium Energy": "#ffb300", "Low Energy": "#388e3c"})
    project_themes = config.get("project_themes", {})
    
    if not os.path.exists(base_backup_path):
        print(f"❌ ERROR: '{base_backup_path}' nahi mili! Pehle app se naya backup export karke root folder me rakh bhai.")
        return False
        
    with open(base_backup_path, 'r', encoding='utf-8') as f:
        sp_data = json.load(f)
        
    db = sp_data.get("data", sp_data.get("state", sp_data))
    if "task" not in db: db["task"] = {"ids": [], "entities": {}}

    project_name = syllabus_data.get("project_name", "New Study Project")
    theme_color = project_themes.get(project_name, "#6495ED") # Dynamic Color!
    project_id = _get_or_create_project(db, project_name, theme_color)

    # 🛡️ Duplicate Task Shield
    existing_tasks = set()
    proj_entities = db["project"]["entities"][project_id]
    all_proj_task_ids = proj_entities.get("taskIds", []) + proj_entities.get("backlogTaskIds", [])
    
    for t_id in all_proj_task_ids:
        if t_id in db["task"]["entities"]:
            existing_tasks.add(db["task"]["entities"][t_id].get("title", "").strip().lower())

    tag_ids = {
        "High": _get_or_create_tag(db, "High Energy", tag_colors.get("High Energy")),
        "Medium": _get_or_create_tag(db, "Medium Energy", tag_colors.get("Medium Energy")),
        "Low": _get_or_create_tag(db, "Low Energy", tag_colors.get("Low Energy"))
    }

    new_task_count = 0
    skipped_count = 0

    for task in syllabus_data.get("tasks", []):
        task_title = task.get("name", "Unnamed").strip()
        
        if task_title.lower() in existing_tasks:
            skipped_count += 1
            continue
            
        duration_mins = task.get("duration", 60)
        energy_req = task.get("energy_req", "Medium")
        assigned_tag = tag_ids.get(energy_req, tag_ids["Medium"])
        notes = task.get("notes", "")
        
        # ⚡ ENGINE LINK: Task generation through sp_models
        sp_task = sp_models.create_sp_task(task_title, duration_mins, project_id, [assigned_tag], notes)
        task_id = sp_task["id"]

        db["task"]["entities"][task_id] = sp_task
        db["task"]["ids"].append(task_id)
        db["project"]["entities"][project_id]["backlogTaskIds"].append(task_id)
        db["tag"]["entities"][assigned_tag]["taskIds"].append(task_id)
        
        new_task_count += 1

    # Wapas pack karna
    with open(out_backup_path, 'w', encoding='utf-8') as f:
        json.dump(sp_data, f, separators=(',', ':'))
        
    print(f"✅ SUCCESS! Created 'vibe-ready.json'. Added: {new_task_count} | Skipped: {skipped_count}")
    
    # Base backup update
    with open(base_backup_path, 'w', encoding='utf-8') as f:
        json.dump(sp_data, f, separators=(',', ':'))
        
    return True