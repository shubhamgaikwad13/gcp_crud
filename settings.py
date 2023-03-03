from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)

PROJECT_ID = os.getenv("project_id")
print(PROJECT_ID)
