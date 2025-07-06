import random
from datetime import datetime
import numpy as np

class FlightDataSimulator:
    """Advanced flight data simulation engine with debugging"""
    
    def __init__(self):
        print("Initializing FlightDataSimulator...")
        self.airlines = [
            {"code": "QF", "name": "Qantas", "base_price": 180, "reliability": 0.95},
            {"code": "VA", "name": "Virgin Australia", "base_price": 160, "reliability": 0.92},
            {"code": "JQ", "name": "Jetstar", "base_price": 120, "reliability": 0.85}
        ]
        
        self.route_network = self._initialize_routes()
        print(f"Initialized with {len(self.route_network)} routes")

    def _initialize_routes(self):
        return {
            "SYD-MEL": {
                "base_demand": 1.4, "distance": 713, "daily_flights": 45,
                "seasonal_factors": {"summer": 1.3, "autumn": 1.0, "winter": 0.9, "spring": 1.1}
            },
            "BNE-SYD": {
                "base_demand": 1.1, "distance": 732, "daily_flights": 32,
                "seasonal_factors": {"summer": 1.2, "autumn": 1.0, "winter": 0.8, "spring": 1.0}
            },
            "PER-SYD": {
                "base_demand": 0.9, "distance": 3285, "daily_flights": 18,
                "seasonal_factors": {"summer": 1.1, "autumn": 0.9, "winter": 0.7, "spring": 1.0}
            }
        }

    def _get_season(self):
        month = datetime.now().month
        if month in [12, 1, 2]: return "summer"
        elif month in [3, 4, 5]: return "autumn"
        elif month in [6, 7, 8]: return "winter"
        else: return "spring"

    def generate_flights(self, origin, destination, date, num_flights=10):
        """Generate mock flights with debug logging"""
        route_key = f"{origin}-{destination}"
        print(f"Generating {num_flights} flights for {route_key} on {date}")
        
        route = self.route_network.get(route_key, {
            "base_demand": 0.8,
            "distance": random.randint(500, 1500),
            "daily_flights": 12,
            "seasonal_factors": {"summer": 1.0, "autumn": 1.0, "winter": 1.0, "spring": 1.0}
        })
        
        season = self._get_season()
        demand_factor = route["base_demand"] * route["seasonal_factors"][season]
        
        flights = []
        for i in range(num_flights):
            airline = random.choices(
                self.airlines,
                weights=[a["reliability"] for a in self.airlines]
            )[0]
            
            base_price = airline["base_price"] * (route["distance"] / 700)
            price_variation = random.gauss(0, 0.15)
            price = base_price * (1 + price_variation) * demand_factor
            
            flights.append({
                "id": f"{route_key}-{i}",
                "airline": airline["name"],
                "flight_number": f"{airline['code']}{random.randint(100, 999)}",
                "departure": f"{random.randint(5, 22):02d}:{random.choice(['00', '15', '30', '45'])}",
                "duration": int(route["distance"] / 500 * 60 + random.randint(-20, 20)),
                "price": round(price, 2),
                "route": route_key,
                "demand_factor": round(demand_factor, 2),
                "aircraft": self._generate_aircraft(route["distance"])
            })
        
        print(f"Generated {len(flights)} flights")
        return sorted(flights, key=lambda x: x["price"])

    def _generate_aircraft(self, distance):
        return "B737" if distance < 800 else random.choice(["B787", "A330"])
    
    def get_route_stats(self):
        """Get route statistics with debug logging"""
        season = self._get_season()
        print(f"Getting route stats for {season} season")
        
        routes = []
        for route, data in self.route_network.items():
            current_demand = round(data["base_demand"] * data["seasonal_factors"][season], 2)
            routes.append({
                "route": route,
                "flights_per_day": data["daily_flights"],
                "current_demand": current_demand,
                "season": season,
                "distance_km": data["distance"],
                "price_trend": "up" if data["seasonal_factors"][season] > 1.1 else "stable"
            })
        
        print(f"Returning stats for {len(routes)} routes")
        return routes