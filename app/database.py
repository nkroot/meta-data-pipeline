import psycopg2
from psycopg2 import DatabaseError
import time
from app.config import settings
from app.common import print_msg,exception_message
"""
Created below method to connect the database connection by Naveen
"""  
def connect(database_hostname,database_name,database_username,database_password):
    try:
        conn = psycopg2.connect(host = database_hostname,database=database_name
                                ,user=database_username,password=database_password
                                
                                )
        print_msg("Databse connection is established")
        return conn

    except (Exception,DatabaseError) as e:
        exception_message(e)

        time.sleep(settings.sleep_time)

        for trycnt in range(settings.retry):
            
            print_msg('The {retrycnt} time of retry'.format(retrycnt=trycnt+1))

            try:
                conn = psycopg2.connect(host = database_hostname,database=database_name
                                ,user=database_username,password=database_password
                                
                                )
                print_msg("Databse connection is established")

                return conn
            except (Exception,DatabaseError) as e:
                exception_message(e)
                time.sleep(settings.sleep_time)
                continue
        raise Exception