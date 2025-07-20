import os
import json
import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # линуксоиды уебаны если что

class Config:
    def __init__(self, name):
        self.name = name
    
    def check(path:str):
        if path.lower().endswith('.json'):
            return "json"
        else:
            return "env"

    def make_path(
            path: str,
            create: bool
    ):
        full_path = os.path.join(BASE_DIR, path)
        
        if not os.path.exists(full_path) and create:
            with open(path, 'w', encoding='utf-8') as f:
                if Config.check(path)=="json":
                    json.dump({}, f, ensure_ascii=False, indent=4)
                else:
                    pass
        else:
            return path
        
    def read(path:str, to_read=None):
        try:
            if Config.check(path)=="json":
                with open(path, "r") as f:
                    if to_read:
                        print(f"[CONFIG---{path}] {to_read} - success")
                        return json.load(f)[to_read]
                    else:   
                        print(f"[CONFIG---{path}] {to_read} - success")
                        return json.load(f)
            else:
                dotenv.load_dotenv(path)
                return os.getenv(to_read, f"{to_read}")
                    
        except:
            print(f"[CONFIG---{path}] couldn't read, provided key - {to_read}") # oopsie woopsie стоило раньше это сделать)


        
    def populate(path, example, to_edit=False):
        if Config.check(path)=="json":
            with open(path,'r', encoding="utf-8") as f:
                data = json.load(f)
                
            required = set(example.keys())
            if not required.issubset(data) and to_edit:
                with open(path, 'w', encoding='utf-8') as f:
                    print(f"saving {root}")
                    json.dump(example, f, ensure_ascii=False, indent=4)
        else:
            existing = dotenv.dotenv_values(path)
            for var,ex in example.items():
                if var in existing:
                    print(f"[CONFIG---{path}] {var} existing, skipping...")
                    continue
                
                tw = os.environ.get(var)
                if tw == None:
                    print(f"[CONFIG---{path}] added {var}")
                    dotenv.set_key(path, var, ex)
            
USERS_PATH = Config.make_path("users.json", True)  # path that have user data for /request_access (rq_acc.py) command
ROOT_PATH = Config.make_path("root_data.env", True)  # path with essential configs for bot to run properly (auto-filled, do not add new objects)
FAQ_PATH = Config.make_path("questions.json",True) # path that have FAQ and answers (auto-filled, do not add new objects)
XRAY_CFG_PATH = Config.make_path("config_xray.json", False)  # path, created by xray service, no need to create this by bot

root = {
    "TOKEN": "DISCORD_BOT_TOKEN",
    "ROOT_ID": "ADMIN_DISCORD_ID",
    "YOOMONEY_ID": "YOOMONEY_WALLET_ID",
    "WEBHOOK_URL": "DISCORD_WEBHOOK_TO_GET_PAYMENTS"
}

users = {
    "DISCORD_ID": {
        "login": "COSMETIC_NAME",
        "proxy1": "PROXY_1",
        "proxy2": "PROXY_2"
    },
}

faq = {
    "CATEGORY": {
        "QUESTION": "ANSWER"
    },
    "CATEGORY2": {
        "QUESTION": "ANSWER"
    }
}

Config.populate(ROOT_PATH, root, True)
Config.populate(FAQ_PATH, faq)
Config.populate(USERS_PATH, users)
