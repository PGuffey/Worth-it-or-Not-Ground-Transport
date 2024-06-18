from process_trip import process_trip
from config import GOOGLE_API_KEY

def main():
    # Prompt user for inputs
    start_address = input("Enter the start address: ")
    end_address = input("Enter the end address: ")
    average_mpg = float(input("Enter the average MPG of your car: "))
    days = int(input("Enter the number of days for the trip calculation (default is 150): ") or 150)
    fuel_type = int(input("Enter the fuel type (1 for Regular, 2 for Midgrade, 3 for Premium): "))

    # Process the trip with the provided inputs
    result = process_trip(start_address, end_address, GOOGLE_API_KEY, average_mpg, days, fuel_type)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Zip codes along the route: {result['zip_codes']}")
        print(f"One-way distance: {result['one_way_distance_miles']} miles")
        print(f"Round-trip distance: {result['round_trip_distance_miles']} miles")
        print(f"One-way estimated time: {result['one_way_time_hours']} hours")
        print(f"Round-trip estimated time: {result['round_trip_time_hours']} hours")
        print(f"Average gas price: {result['average_gas_price']} USD")
        print(f"Low gas price: {result['low_gas_price']} USD")
        print(f"High gas price: {result['high_gas_price']} USD")
        print(f"Average cost per one-way trip: {result['avg_cost_per_one_way']} USD")
        print(f"Average cost per round-trip: {result['avg_cost_per_round_trip']} USD")
        print(f"Total cost for {days} days: {result['avg_total_cost']} USD")
        print(f"Low cost per one-way trip: {result['low_cost_per_one_way']} USD")
        print(f"Low cost per round-trip: {result['low_cost_per_round_trip']} USD")
        print(f"Total low cost for {days} days: {result['low_total_cost']} USD")
        print(f"High cost per one-way trip: {result['high_cost_per_one_way']} USD")
        print(f"High cost per round-trip: {result['high_cost_per_round_trip']} USD")
        print(f"Total high cost for {days} days: {result['high_total_cost']} USD")

if __name__ == "__main__":
    main()
