from app.common import exception_message
from app.database import DatabaseConn 
from psycopg2 import DatabaseError
from app.datamovement.weather_details import WeatherDetails 
from app.config import settings
import sys
from app.jobs.agg_details import AggDetails 



if __name__ =="__main__":
    try:
        #Connecting to the database
        dbc = DatabaseConn()
        conn = dbc.connect(settings.database_hostname,settings.database_name,settings.database_username,settings.database_password)
        
        # Getting the values from the user
        latitude = sys.argv[1]
        longitude = sys.argv[2]
        
        wd = WeatherDetails()
        wd.execute(conn,latitude,longitude)

        agg=AggDetails()
        agg.execute(conn)
        conn.close()
    except (Exception,DatabaseError) as err:
        exception_message(err)      
        