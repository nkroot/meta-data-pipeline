from app.common import timeit,log,exception_message
from psycopg2 import DatabaseError

class AggDetails(object):

    def __init__(self) -> None:
        pass
    
    #location, date and temperature of the highest temperatures reported by location and month
    @timeit
    def agg_max_temp_location(self,conn):

        with conn.cursor() as cursor:
            try:
                #truncating the table to receive only recent information
                sql="""truncate table dev.agg_max_temp_location restart identity """
                log(sql)
                cursor.execute(sql)

                sql = """
                    INSERT INTO dev.agg_max_temp_location (latitude,longitude,location,date_of_reading,temperature)
                    select distinct latitude,
                                longitude,location,date(date_time) as dt,temperature
                        from (
                        select  
                                latitude,
                                longitude,
                                location,
                                date_time,
                                temperature,
                                max(temperature) over(partition by latitude,longitude,Extract(Month from date_time) 
                                                    order by latitude,longitude,Extract(Month from date_time) ) as highest_temp
                        from 	staging.stg_weather_detail_info
                        )a
                        where temperature = highest_temp;"""
                
                log(sql)
                cursor.execute(sql)
                conn.commit()
                log("""dev.agg_max_temp_location table is populated""",level='info')
            except (Exception,DatabaseError) as err:
                exception_message(err)

    #average temperature, min temperature, location of min temperature, and location of max temperature per day
    @timeit
    def agg_weather_details(self,conn):

        try:

            with conn.cursor() as cursor:
                
                sql = """truncate table dev.agg_weather_details restart identity """
                log(sql)
                cursor.execute(sql)
                
                sql = """
                    INSERT INTO dev.agg_weather_details (date_of_reading,avg_temperature,min_temperature,min_temp_latitude,min_temp_longitude,
                                                        max_temp_latitude,max_temp_longitude)
                    select 	
                            date_of_recording,
                            avg_temperature,
                            min_temperature,
                            --max_temperature,
                            mint.latitude min_temp_latitude,
                            mint.longitude  min_temp_longitude,
                            maxt.latitude  max_temp_latitude,
                            maxt.longitude  max_temp_longitude

                    from ( 
                        select  date(date_time) date_of_recording,
                                Avg(temperature) as avg_temperature,
                                min(temperature) as min_temperature,
                                max(temperature) as max_temperature
                        from 	staging.stg_weather_detail_info
                        group by date(date_time)
                        )agg 
                    left join staging.stg_weather_detail_info mint on date(mint.date_time)= agg.date_of_recording 
                                                                    and agg.min_temperature = mint.temperature  
                    left join staging.stg_weather_detail_info maxt on date(maxt.date_time)= agg.date_of_recording 
                                                                    and agg.max_temperature = maxt.temperature 
                    ;"""

                log(sql)
                cursor.execute(sql)
                conn.commit()
                log("""dev.agg_weather_details table is populated""",level='info')
        except (Exception,DatabaseError) as err:
                exception_message(err)

    def execute(self,conn):
        
        self.agg_max_temp_location(conn)
        self.agg_weather_details(conn)
    