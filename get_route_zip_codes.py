import requests

def get_route_zip_codes_distance_time(start_address, end_address, google_api_key):
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_address}&destination={end_address}&key={google_api_key}"
    directions_response = requests.get(directions_url)
    directions_data = directions_response.json()
    
    if directions_data['status'] != 'OK':
        raise Exception(f"Error fetching directions: {directions_data['status']}")

    route_steps = directions_data['routes'][0]['legs'][0]['steps']
    coordinates = [(step['start_location']['lat'], step['start_location']['lng']) for step in route_steps]

    zip_codes = set()
    for lat, lng in coordinates:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={google_api_key}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] != 'OK':
            continue

        for component in geocode_data['results'][0]['address_components']:
            if 'postal_code' in component['types']:
                zip_codes.add(component['long_name'])
                break

    total_distance_meters = directions_data['routes'][0]['legs'][0]['distance']['value']
    total_distance_km = total_distance_meters / 1000
    total_time_seconds = directions_data['routes'][0]['legs'][0]['duration']['value']
    total_time_hours = total_time_seconds / 3600

    return list(zip_codes), total_distance_km, total_time_hours
