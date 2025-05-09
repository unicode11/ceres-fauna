import os
from json import dump

# making paths for nonexistant files or checking if they exist i dunno fkoff
# LAGGY AS FUCK
# def make_path(path: str | Path):
#     created_path = Path(path)
#     created_path.touch(exist_ok=True)
#     return created_path

def make_path(filepath: str):
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            if filepath.lower().endswith('.json'):
                dump({},f, ensure_ascii=False, indent=4)
            else:
                pass
    else:
        return filepath

USERS_PATH = make_path("users.json")
ROOT_PATH = make_path("root_data.json")

