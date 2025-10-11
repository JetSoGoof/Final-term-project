DB_PATH = os.environ.get("MONEYHYPE_DB")
if not DB_PATH:
    DATA_DIR = user_data_dir()
    os.makedirs(DATA_DIR, exist_ok=True)
    DB_PATH = os.path.join(DATA_DIR, "db.json")