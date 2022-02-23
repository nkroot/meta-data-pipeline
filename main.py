from app.common import exception_message
from app.database import connect
from psycopg2 import DatabaseError
from app.datamovement import weather_details as wd
from app.config import settings
import sys
from app.jobs import agg_details as agg



if __name__ =="__main__":
    try:
        
        conn = connect(settings.database_hostname,settings.database_name,settings.database_username,settings.database_password)

        latitude = sys.argv[1]
        longitude = sys.argv[2]
        wd.execute(conn,latitude,longitude)

        agg.execute(conn)
        
    except (Exception,DatabaseError) as err:
        exception_message(err)
    finally:
        
        conn.close()