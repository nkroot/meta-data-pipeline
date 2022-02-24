import psycopg2
from psycopg2 import DatabaseError
import time
from app.config import settings
from app.common import print_msg,exception_message,log
"""
Created below method to connect the database connection by Naveen
"""  
def connect(database_hostname,database_name,database_username,database_password):
    try:
        conn = psycopg2.connect(host = database_hostname,database=database_name
                                ,user=database_username,password=database_password
                                
                                )
        log("Databse connection is established",level='info')
        
        return conn

    except (Exception,DatabaseError) as e:
        exception_message(e)

        time.sleep(settings.sleep_time)

        for trycnt in range(settings.retry):
            
            log("The {retrycnt} time of retry".format(retrycnt=trycnt+1),level="info")
            
            try:
                conn = psycopg2.connect(host = database_hostname,database=database_name
                                ,user=database_username,password=database_password
                                
                                )
                log("Databse connection is established",level="info")

                return conn
            except (Exception,DatabaseError) as e:
                exception_message(e)
                time.sleep(settings.sleep_time)
                continue
        raise Exception