import configs.config as config
from sqlalchemy import create_engine

dbconfig = config.configs.db
DATABASE_URL = f"mysql+pymysql://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['database']}?charset=utf8mb4"

print(DATABASE_URL)
