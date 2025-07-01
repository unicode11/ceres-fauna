import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # линуксоиды уебаны если что

def make_path(
        filepath: str,
        create: bool
):
    full_path = os.path.join(BASE_DIR, filepath)
    
    if not os.path.exists(full_path) and create:
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
        f"couldn't read {path}" # oopsie woopsie стоило раньше это сделать)

    
def populate(config_file, config_json_example, to_edit=False):
    with open(config_file,'r', encoding="utf-8") as f:
        data = json.load(f)
        
    required = set(config_json_example.keys())
    if not required.issubset(data) and to_edit:
        with open(config_file, 'w', encoding='utf-8') as f:
            print(f"saving {root}")
            json.dump(config_json_example, f, ensure_ascii=False, indent=4)
            
USERS_PATH = make_path("users.json", True)  # path that will be created by "add_user" command
ROOT_PATH = make_path("root_data.json", True)  # path with essential configs for bot to run properly (auto-filled, do not add new objects)
FAQ_PATH = make_path("questions.json",True) # path that have FAQ and answers (auto-filled, do not add new objects)
XRAY_CFG_PATH = make_path("config_xray.json", False)  # path, created by xray service, no need to create this by bot

root = {
    "token": "BOT_TOKEN_HERE",
    "root_id": "ADMIN_DISCORD_ID",
    "yoomoney_id": "YOOMONEY_WALLET_ID",
    "webhook": "DISCORD_WEBHOOK_TO_GET_PAYMENTS"
}

faq = {
    "CATEGORY": {
        "QUESTION": "ANSWER"
    },
    "CATEGORY2": {
        "QUESTION": "ANSWER"
    }
}

populate(ROOT_PATH, root, True)
populate(FAQ_PATH, faq)
