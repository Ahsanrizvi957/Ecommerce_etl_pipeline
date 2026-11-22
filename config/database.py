import os
from sqlalchemy import create_engine

def get_database_engine():
    
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "database_url is missing "
        )
    return create_engine(database_url,pool_pre_ping = True)