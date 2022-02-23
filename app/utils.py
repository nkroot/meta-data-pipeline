from geopy.geocoders import Nominatim
  

def get_location(latitude,longitude)->str:

    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
    # Latitude & Longitude input   
    location = geolocator.reverse(str(latitude)+","+str(longitude))
    
    return location.raw['address'].get('city', 'unknown')
    
   