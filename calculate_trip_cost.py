def calculate_trip_cost(mpg, distance_miles, gas_price_per_gallon, days=150):
    cost_per_one_way = (distance_miles / mpg) * gas_price_per_gallon
    cost_per_round_trip = cost_per_one_way * 2
    total_cost = cost_per_round_trip * days
    
    return cost_per_one_way, cost_per_round_trip, total_cost
