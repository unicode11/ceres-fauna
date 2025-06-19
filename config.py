import os
import json

def make_path(
        filepath: str,
        create: bool
):
    if not os.path.exists(filepath) and create:
        with open(filepath, 'w', encoding='utf-8') as f:
            if filepath.lower().endswith('.json'):
                json.dump({}, f, ensure_ascii=False, indent=4)
            else:
                pass
    else:
        return filepath
    
def read(path:str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        "couldn't read"
    
def populate_root():
    with open(ROOT_PATH,'r', encoding="utf-8") as f:
        data = json.load(f)
        
    penis = {
        "token": "BOT_TOKEN_HERE",
        "root_id": "ADMIN_DISCORD_ID"
    }
    
    required = {"token","root_id"}
    if not required.issubset(data):
        with open(ROOT_PATH, 'w', encoding='utf-8') as f:
            print(f"saving {penis}")
            json.dump(penis, f, ensure_ascii=False, indent=4)
        
# no edit above

USERS_PATH = make_path("users.json", True)  # path that will be created by "add_user" command
ROOT_PATH = make_path("root_data.json", True)  # path that have bot token and root user discord ID
XRAY_CFG_PATH = make_path("config_xray.json", False)  # path, created by xray service, no need to create this by bot

# no edit below

populate_root()
