from get_route_zip_codes import get_route_zip_codes_distance_time
from get_gas_prices import get_gas_prices
from calculate_trip_cost import calculate_trip_cost

def process_trip(start_address, end_address, google_api_key, average_mpg, days=150, fuel_type=1):
    try:
        zip_codes, one_way_distance_km, one_way_time_hours = get_route_zip_codes_distance_time(start_address, end_address, google_api_key)
        one_way_distance_miles = one_way_distance_km * 0.621371
        round_trip_distance_miles = one_way_distance_miles * 2
        round_trip_time_hours = one_way_time_hours * 2
        
        gas_prices = []
        for zip_code in zip_codes:
            try:
                cash_prices, credit_prices = get_gas_prices(zip_code, fuel_type)
                gas_prices.extend(cash_prices)
                gas_prices.extend(credit_prices)
            except Exception as e:
                print(f"Error fetching gas prices for {zip_code}: {e}")
        
        if gas_prices:
            average_gas_price = sum(gas_prices) / len(gas_prices)
            low_gas_price = min(gas_prices)
            high_gas_price = max(gas_prices)

            avg_cost_per_one_way, avg_cost_per_round_trip, avg_total_cost = calculate_trip_cost(average_mpg, one_way_distance_miles, average_gas_price, days)
            low_cost_per_one_way, low_cost_per_round_trip, low_total_cost = calculate_trip_cost(average_mpg, one_way_distance_miles, low_gas_price, days)
            high_cost_per_one_way, high_cost_per_round_trip, high_total_cost = calculate_trip_cost(average_mpg, one_way_distance_miles, high_gas_price, days)

            return {
                "zip_codes": zip_codes,
                "one_way_distance_miles": one_way_distance_miles,
                "round_trip_distance_miles": round_trip_distance_miles,
                "one_way_time_hours": one_way_time_hours,
                "round_trip_time_hours": round_trip_time_hours,
                "average_gas_price": average_gas_price,
                "low_gas_price": low_gas_price,
                "high_gas_price": high_gas_price,
                "avg_cost_per_one_way": avg_cost_per_one_way,
                "avg_cost_per_round_trip": avg_cost_per_round_trip,
                "avg_total_cost": avg_total_cost,
                "low_cost_per_one_way": low_cost_per_one_way,
                "low_cost_per_round_trip": low_cost_per_round_trip,
                "low_total_cost": low_total_cost,
                "high_cost_per_one_way": high_cost_per_one_way,
                "high_cost_per_round_trip": high_cost_per_round_trip,
                "high_total_cost": high_total_cost,
            }
        else:
            return {"error": "No gas prices found for the route."}
    
    except Exception as e:
        return {"error": str(e)}
