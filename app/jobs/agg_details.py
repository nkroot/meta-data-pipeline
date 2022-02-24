from app.common import print_msg, timeit


@timeit
def agg_max_temp_location(conn):

    with conn.cursor() as cursor:

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
        cursor.execute("""truncate table dev.agg_max_temp_location restart identity """)
        
        cursor.execute(sql)
        conn.commit()


@timeit
def agg_weather_details(conn):

    with conn.cursor() as cursor:

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

        cursor.execute("""truncate table dev.agg_weather_details restart identity """)
        
        cursor.execute(sql)
        conn.commit()
        
        cursor.execute("""select count(1) as cnt from staging.stg_weather_detail_info""")
        dag = cursor.fetchone()
        print_msg(dag[0])

def execute(conn):
    agg_max_temp_location(conn)
    agg_weather_details(conn)
    