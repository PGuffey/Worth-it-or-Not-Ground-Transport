import requests
import json

def get_gas_prices(zip_code, fuel_type=1):
    url = "https://www.gasbuddy.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    payload = {
        "operationName": "LocationBySearchTerm",
        "variables": {
            "search": zip_code
        },
        "query": """
        query LocationBySearchTerm($search: String) {
            locationBySearchTerm(search: $search) {
                stations {
                    results {
                        fuels
                        prices {
                            cash {
                                price
                            }
                            credit {
                                price
                            }
                        }
                    }
                }
            }
        }
        """
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()

        # Initialize lists to store prices
        cash_prices = []
        credit_prices = []

        # Extract the relevant data
        location_data = data.get('data', {}).get('locationBySearchTerm', {})
        if not location_data:
            print("No location data found.")
            return cash_prices, credit_prices

        stations = location_data.get('stations', {}).get('results', [])
        if not stations:
            print("No stations found.")
            return cash_prices, credit_prices
        
        fuel_type_map = {1: "regular_gas", 2: "midgrade_gas", 3: "premium_gas"}
        selected_fuel = fuel_type_map.get(fuel_type, "regular_gas")

        for station in stations:
            fuels = station.get('fuels', [])
            prices = station.get('prices', [])
            for fuel, price_info in zip(fuels, prices):
                if fuel == selected_fuel:
                    cash_price = price_info.get('cash', {}).get('price') if price_info.get('cash') else None
                    credit_price = price_info.get('credit', {}).get('price') if price_info.get('credit') else None
                    if cash_price is not None and cash_price > 0:
                        cash_prices.append(cash_price)
                    if credit_price is not None and credit_price > 0:
                        credit_prices.append(credit_price)

        return cash_prices, credit_prices
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch gas prices: {e}")
        return [], []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], []
