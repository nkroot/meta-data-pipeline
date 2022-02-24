from typing import Dict,Iterator,Any
from urllib.parse import urlencode
import requests
import calendar
from datetime import datetime,timedelta
from app.common import clean_csv_value,StringIteratorIO,timeit,date_unixtimestamp_gmt,exception_message,log
from app.sqlmodule import get_existing_hashed_data
from  psycopg2 import DatabaseError
from app.config import settings
from app.utils import get_location

class WeatherDetails(object):

    def __init__(self) -> None:
        pass
    
    #Created to fetch the last 5 days json from the API
    def iterate_api_for_temperature_info (self,latitude: float,longitude:float) -> Iterator[Dict[str, Any]]:
        session = requests.Session()
        apikey=settings.apikey
        #Iterating to fetch last 5 days of data
        for i in range(1,6):
            
            #Generating unix timestamp from UTC time zone
            response_dt = datetime.utcnow()+timedelta(days=-i)
            unixtimestamp = calendar.timegm(response_dt.utctimetuple())
            
            response = session.get('http://api.openweathermap.org/data/2.5/onecall/timemachine?' + urlencode({
                'lat': latitude,
                'lon': longitude,
                'dt': unixtimestamp,
                'appid': apikey
                    }),).json()

            #Created as a geerator to save the memory
            yield response

    #Created the method to save the data through CSV file into postgres db using generators
    @timeit
    def write_json_data_to_weather_stg_table(self,conn :str, weather_info: Iterator[Dict[str, Any]],location:str,size: int = 8192) -> None:

        try:
            
            table_name = 'stg_weather_detail_info'
            col_name = "latitude,longitude,unixtimestamp"    
            log(table_name,level='info')
            with conn.cursor() as cursor:
                
                #Setting the database for execution 
                sql = "SET search_path TO %s "%(settings.staging_schema)
                log(sql)
                cursor.execute("SET search_path TO %s ",(settings.staging_schema,))

                existing_data = get_existing_hashed_data(cursor,table_name,col_name)
                
                #Creating CSV file like string
                weather_string_iterator = StringIteratorIO((
                                '|'.join(map(clean_csv_value, (
                                    weather_dict['lat'],
                                    weather_dict['lon'],
                                    location,
                                    weather_dict['timezone'],
                                    weather_dict['timezone_offset'],
                                    hourly_dict['dt'],
                                    date_unixtimestamp_gmt(hourly_dict['dt']),
                                    date_unixtimestamp_gmt(weather_dict['current']['sunrise']),
                                    date_unixtimestamp_gmt(weather_dict['current']['sunset']),
                                    hourly_dict['temp'],
                                    hourly_dict['feels_like'],
                                    hourly_dict['pressure'],
                                    hourly_dict['humidity'],
                                    hourly_dict['dew_point'],
                                    hourly_dict['uvi'],
                                    hourly_dict['clouds'],
                                    hourly_dict['visibility'],
                                    hourly_dict['wind_speed'],
                                    hourly_dict['wind_deg'],
                                    hourly_dict.get('wind_gust',0.0),
                                    hourly_dict['weather'][0]['id'],
                                    hourly_dict['weather'][0]['main'],
                                    hourly_dict['weather'][0]['description'],
                                    hourly_dict.get('rain',{}).get('1h',0.00),
                                    hourly_dict.get('snow',{}).get('1h',0.00),
                                
                                ))) + '\n'
                                for weather_dict in weather_info
                                for hourly_dict in weather_dict["hourly"]
                                if hash((str(weather_dict['lat']),
                                    str(weather_dict['lon']),str(hourly_dict['dt']))) not in existing_data
                                ))
            
                #Copying the data to postgres using CSV with required fields
                cursor.copy_from( weather_string_iterator, table_name, sep='|',
                                    size = size,
                                    columns=('latitude','longitude','location','timezone','timezone_offset','unixtimestamp','date_time','sunrise',
                                            'sunset','temperature','temp_feels_like','atm_pressure_hpa','humidity_percent','dew_point',
                                            'uv_index','clouds_percent','visibility_meters','wind_speed','wind_deg','wind_gust'
                                            ,'condition_id',
                                            'weather_group','description','rain_volume_mm','snow_volume_mm'
                                            ))
                conn.commit()
        except (Exception,DatabaseError) as err:
            exception_message(err)


    def execute(self,conn,latitude,longitude):
        
        #Iterating the generator 
        weather_info=list(self.iterate_api_for_temperature_info(latitude,longitude))
        
        #Identify the city name based on the latitudes and longitudes
        location = get_location(latitude,longitude)

        #writing the data into postgres
        log("Data Insertion Started",level='info')
        self.write_json_data_to_weather_stg_table(conn,weather_info,location)
        log("Data Insertion Ended",level='info')