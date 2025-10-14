# database
import os
from tinydb import TinyDB, Query
from utils import user_data_dir

DB_PATH = os.environ.get("MONEYHYPE_DB")
if not DB_PATH:
    DATA_DIR = user_data_dir()
    os.makedirs(DATA_DIR, exist_ok=True)
    DB_PATH = os.path.join(DATA_DIR, "db.json")

db = TinyDB(DB_PATH)
T_TXNS = db.table("transactions")
T_SAV  = db.table("savings")
T_SPL  = db.table("splits")
Q = Query()