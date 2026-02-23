import json
import uuid
import time
import os

def generate_sp_id():
    return str(uuid.uuid4())[:21]

def _get_or_create_tag(db, tag_name, color):
    if "tag" not in db: db["tag"] = {"ids": [], "entities": {}}
    tags = db.get("tag", {}).get("entities", {})
    
    for t_id, t_data in tags.items():
        if t_data.get("title", "").strip().lower() == tag_name.strip().lower():
            return t_id
            
    print(f"   🏷️ Creating Tag: '{tag_name}'")
    new_tag_id = generate_sp_id()
    db["tag"]["entities"][new_tag_id] = {
        "id": new_tag_id, "title": tag_name, "icon": "bolt", "color": color,
        "created": int(time.time() * 1000), "modified": int(time.time() * 1000), "taskIds": []
    }
    db["tag"]["ids"].append(new_tag_id)
    return new_tag_id

def _get_or_create_project(db, project_name):
    if "project" not in db: db["project"] = {"ids": [], "entities": {}}
    projects = db.get("project", {}).get("entities", {})
    
    for p_id, p_data in projects.items():
        if p_data.get("title", "").strip().lower() == project_name.strip().lower():
            return p_id
            
    print(f"   🏗️ Creating Project: '{project_name}'")
    new_proj_id = generate_sp_id()
    db["project"]["entities"][new_proj_id] = {
        "id": new_proj_id, "title": project_name, "isHiddenFromMenu": False, 
        "isArchived": False, "isEnableBacklog": True, "backlogTaskIds": [], 
        "noteIds": [], "taskIds": [], "icon": "library_books",
        "theme": { "primary": "#6495ED", "isAutoContrast": True, "backgroundOverlayOpacity": 0 }
    }
    db["project"]["ids"].append(new_proj_id)
    
    if "menuTree" not in db: db["menuTree"] = {"projectTree": [], "tagTree": []}
    if "projectTree" not in db["menuTree"]: db["menuTree"]["projectTree"] = []
    db["menuTree"]["projectTree"].append({"k": "p", "id": new_proj_id})
    return new_proj_id

def inject_syllabus(syllabus_data, sync_file_path):
    print(f"\n💉 Reading base-backup.json for: {syllabus_data.get('project_name', 'Unknown')}")
    
    root_dir = os.path.dirname(sync_file_path)
    base_backup_path = os.path.join(root_dir, "base-backup.json")
    out_backup_path = os.path.join(root_dir, "vibe-ready.json")
    
    if not os.path.exists(base_backup_path):
        print(f"❌ ERROR: '{base_backup_path}' nahi mili! Pehle app se naya backup export karke root folder me rakh bhai.")
        return False
        
    with open(base_backup_path, 'r', encoding='utf-8') as f:
        sp_data = json.load(f)
        
    # Smart Data Extractor (Backup ho ya Sync file, dono handle karega)
    db = sp_data.get("data", sp_data.get("state", sp_data))
    if "task" not in db: db["task"] = {"ids": [], "entities": {}}

    project_name = syllabus_data.get("project_name", "New Study Project")
    project_id = _get_or_create_project(db, project_name)

    # 🛡️ Duplicate Task Shield
    existing_tasks = set()
    proj_entities = db["project"]["entities"][project_id]
    all_proj_task_ids = proj_entities.get("taskIds", []) + proj_entities.get("backlogTaskIds", [])
    
    for t_id in all_proj_task_ids:
        if t_id in db["task"]["entities"]:
            existing_tasks.add(db["task"]["entities"][t_id].get("title", "").strip().lower())

    tag_ids = {
        "High": _get_or_create_tag(db, "High Energy", "#e11826"),
        "Medium": _get_or_create_tag(db, "Medium Energy", "#ffb300"),
        "Low": _get_or_create_tag(db, "Low Energy", "#388e3c")
    }

    new_task_count = 0
    skipped_count = 0
    current_time_ms = int(time.time() * 1000)

    for task in syllabus_data.get("tasks", []):
        task_title = task.get("name", "Unnamed").strip()
        
        if task_title.lower() in existing_tasks:
            skipped_count += 1
            continue
            
        task_id = generate_sp_id()
        duration_ms = task.get("duration", 60) * 60 * 1000
        assigned_tag = tag_ids.get(task.get("energy_req", "Medium"), tag_ids["Medium"])
        
        sp_task = {
            "id": task_id, "subTaskIds": [], "timeSpentOnDay": {}, "timeSpent": 0,
            "timeEstimate": duration_ms, "isDone": False, "title": task_title, 
            "notes": task.get("notes", ""), "tagIds": [assigned_tag], 
            "created": current_time_ms, "projectId": project_id, "attachments": [], "dueDay": None
        }

        db["task"]["entities"][task_id] = sp_task
        db["task"]["ids"].append(task_id)
        db["project"]["entities"][project_id]["backlogTaskIds"].append(task_id)
        db["tag"]["entities"][assigned_tag]["taskIds"].append(task_id)
        
        new_task_count += 1
        current_time_ms += 1

    # Wapas original structure mein pack karna
    with open(out_backup_path, 'w', encoding='utf-8') as f:
        json.dump(sp_data, f, separators=(',', ':'))
        
    print(f"✅ SUCCESS! Created 'vibe-ready.json'. Added: {new_task_count} | Skipped: {skipped_count}")
    
    # Base backup ko update karo taaki ek sath 4 json phenko toh fail na ho
    with open(base_backup_path, 'w', encoding='utf-8') as f:
        json.dump(sp_data, f, separators=(',', ':'))
        
    return True