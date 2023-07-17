

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
SECRET_PHRASE=os.getenv('DB_USER')
print(SECRET_PHRASE)
