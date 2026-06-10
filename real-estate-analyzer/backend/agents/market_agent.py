from services.attom_service import get_property_detail
from services.census_service import get_demographics


async def run_market_agent(address: str) -> dict:
    property_detail = await get_property_detail(address)
    demographics = await get_demographics(address)
    subject_vs_market_pct = (
        (property_detail["property_value"] - property_detail["zip_median_price"])
        / property_detail["zip_median_price"]
        * 100
    )
    return {
        "median_price": property_detail["zip_median_price"],
        "city_avg_price": property_detail["city_avg_price"],
        "price_per_sqft": property_detail["price_per_sqft"],
        "subject_value": property_detail["property_value"],
        "subject_vs_market_pct": round(subject_vs_market_pct, 1),
        "trend_direction": "Upward",
        "comp_properties": property_detail["comps"],
        "neighborhood_score": 82,
        "demographics": demographics,
        "property": property_detail,
    }

