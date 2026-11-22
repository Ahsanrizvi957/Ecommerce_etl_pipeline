import time
from datetime import datetime,timezone
from sqlalchemy import text


def create_audit_table(engine):
    
    query = text("""
    CREATE TABLE IF NOT EXISTS stagging.audit_log(
        audit_id SERIAL PRIMARY KEY,
        table_name VARCHAR(30),
        load_start TIME,
        load_end TIME,
        rows_loaded INTEGER,
        duration NUMERIC(10,2),
        status VARCHAR(30),
        error_message TEXT
    );
""")
    with engine.begin() as connection:
        connection.execute(query)

def load_with_audit(df,table_name,engine,schema = 'stagging'):

    start_time = datetime.now(timezone.utc)
    start_counter = time.perf_counter()

    status = 'Success'
    error_message = None
    rows_loaded = 0

    try:
        df.to_sql(
            name = table_name,
            con = engine,
            schema = schema,
            if_exists = 'replace',
            index = False
        )
        print(f"loaded {len(df)} rows into {table_name}")
        
        rows_loaded = len(df)

    except Exception as error:
        
        status = 'Failed',
        error_message = str(error)
        raise

    finally:
        
        end_time = datetime.now(timezone.utc)
        end_counter = time.perf_counter()
        duration = round(end_counter - start_counter, 2)
        
        audit_query = text("""
            INSERT INTO stagging.audit_log(
                
                table_name,
                load_start,
                load_end,
                rows_loaded,
                duration,
                status,
                error_message
            )
            VALUES(
                
                :table_name,
                :load_start,
                :load_end,
                :rows_loaded,
                :duration,
                :status,
                :error_message
            
            );
        """)
        with engine.begin() as connection:
            connection.execute(
                audit_query,
                {
            
                "table_name": table_name,
                "load_start": start_time,
                "load_end": end_time,
                "rows_loaded": rows_loaded,
                "duration": duration,
                "status": status,
                "error_message": error_message
                }
            )