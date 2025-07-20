import os
import json
import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # линуксоиды уебаны если что

class Config:
    def __init__(self, name):
        self.name = name
    
    def Check(path:str):
        if path.lower().endswith('.json'):
            return "json"
        else:
            return "env"

    def MakePath(
            path: str,
            create: bool=True
    ):
        full_path = os.path.join(BASE_DIR, path)
        
        if not os.path.exists(full_path) and create:
            with open(path, 'w', encoding='utf-8') as f:
                if Config.Check(path)=="json":
                    json.dump({}, f, ensure_ascii=False, indent=4)
                else:
                    pass
        else:
            return path
        
    def Read(path:str, to_read=None):
        try:
            if Config.Check(path)=="json":
                with open(path, "r") as f:
                    print(f"[CONFIG---{path}] {to_read} - success")
                    return json.load(f)
            else:
                dotenv.load_dotenv(path)
                print(f"[CONFIG---{path}] {to_read} - success")
                return os.getenv(to_read, f"{to_read}")
                    
        except:
            print(f"[CONFIG---{path}] couldn't read, provided key - {to_read}")


        
    def Fill(path, example):
        if Config.Check(path)=="json":
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"[CONFIG---{path}] ERROR")
                return

            updated = False
            for key, value in example.items():
                if key not in data:
                    data[key] = value
                    updated = True

            if updated:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"[CONFIG---{path}] добавлены недостающие ключи:\n{data}\nsuccess")
                    
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
            
USERS_PATH = Config.MakePath("users.json")  # path that have user data for /request_access (rq_acc.py) command
ROOT_PATH = Config.MakePath("root_data.env")  # path with essential configs for bot to run properly (auto-filled, do not add new objects)
FAQ_PATH = Config.MakePath("questions.json") # path that have FAQ and answers (auto-filled, do not add new objects)
DIFF_PATH = Config.MakePath("diff.json") # path that contains various answers for different commands
# XRAY_CFG_PATH = Config.MakePath("config_xray.json", False)  # path, created by xray service, no need to create this by bot

Config.Fill(ROOT_PATH, {
"TOKEN": "DISCORD_BOT_TOKEN",
"ROOT_ID": "ADMIN_DISCORD_ID",
"YOOMONEY_ID": "YOOMONEY_WALLET_ID",
"WEBHOOK_URL": "DISCORD_WEBHOOK_TO_GET_PAYMENTS"})

Config.Fill(FAQ_PATH, {
    "CATEGORY": {
        "QUESTION": "ANSWER"
    },
    "CATEGORY2": {
        "QUESTION": "ANSWER"
    }
})

Config.Fill(USERS_PATH, {
"DISCORD_ID": {
    "login": "COSMETIC_NAME",
    "proxy1": "PROXY_1",
    "proxy2": "PROXY_2"
}})

Config.Fill(DIFF_PATH, {
    "CATEGORY":
    [
        "ANSWER_1",
        "ANSWER_2"
    ]
})
