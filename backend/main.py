import re
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
from mock_engine.data_simulator import FlightDataSimulator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
simulator = FlightDataSimulator()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlightRequest(BaseModel):
    origin: str
    destination: str
    date: str
    return_date: Optional[str] = None

@app.post("/api/flights")
async def get_flights(request: FlightRequest):
    try:
        logger.info(f"Received request: {request.dict()}")
        
        # Validate inputs
        if len(request.origin) != 3 or len(request.destination) != 3:
            raise HTTPException(
                status_code=422,
                detail="Airport codes must be 3 characters"
            )
            
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', request.date):
            raise HTTPException(
                status_code=422,
                detail="Date must be in YYYY-MM-DD format"
            )

        if request.return_date and not re.match(r'^\d{4}-\d{2}-\d{2}$', request.return_date):
            raise HTTPException(
                status_code=422,
                detail="Return date must be in YYYY-MM-DD format"
            )

        flights = simulator.generate_flights(
            request.origin.upper(),
            request.destination.upper(),
            request.date,
            random.randint(8, 15)
        )
        
        if request.return_date:
            return_flights = simulator.generate_flights(
                request.destination.upper(),
                request.origin.upper(),
                request.return_date,
                random.randint(5, 10)
            )
            flights.extend(return_flights)
        
        logger.info(f"Generated {len(flights)} flights")
        
        return {
            "data": flights,
            "insights": generate_insights(flights),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "num_flights": len(flights)
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/popular-routes")
async def popular_routes():
    try:
        logger.info("Fetching popular routes")
        routes = simulator.get_route_stats()
        
        return JSONResponse({
            "routes": routes,
            "seasonal_advice": get_seasonal_tips(routes[0]["season"] if routes else "summer"),
            "debug": {
                "num_routes": len(routes),
                "generated_at": datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Error fetching routes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def generate_insights(flights):
    """Generate insights with debug logging"""
    if not flights:
        return {"error": "No flight data available"}
    
    prices = [f["price"] for f in flights]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    
    logger.debug(f"Price analysis - Avg: {avg_price:.2f}, Range: {min_price}-{max_price}")
    
    return {
        "price_summary": {
            "average": round(avg_price, 2),
            "min": min_price,
            "max": max_price,
            "trend": "decreasing" if avg_price < (sum(prices[:3]) / 3) else "increasing"
        },
        "recommendation": "Book now" if avg_price < 200 else "Wait for better deals",
        "airlines": list({f["airline"] for f in flights})
    }

def get_seasonal_tips(season):
    tips = {
        "summer": "Book at least 2 weeks early for peak season travel",
        "winter": "Last-minute deals often available",
        "spring": "Flexible dates can save up to 20%",
        "autumn": "Ideal time for business travel"
    }
    return tips.get(season, "Good time to travel")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")