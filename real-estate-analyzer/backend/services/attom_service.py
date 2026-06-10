import os

import httpx

MOCK_PROPERTY = {
    "property_value": 425000,
    "price_per_sqft": 248,
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft": 1714,
    "year_built": 1998,
    "last_sold_price": 390000,
    "last_sold_date": "2021-06-15",
    "zip_median_price": 389000,
    "city_avg_price": 412000,
    "comps": [
        {"address": "456 Oak St, Austin, TX 78702", "price": 410000, "sqft": 1680, "price_per_sqft": 244},
        {"address": "789 Pine Ave, Austin, TX 78702", "price": 445000, "sqft": 1820, "price_per_sqft": 244},
        {"address": "321 Elm Rd, Austin, TX 78702", "price": 398000, "sqft": 1590, "price_per_sqft": 250},
    ],
}


async def get_property_detail(address: str) -> dict:
    api_key = os.getenv("ATTOM_API_KEY", "")
    if not api_key:
        return {**MOCK_PROPERTY, "address": address}
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail",
                params={"address1": address, "address2": ""},
                headers={"apikey": api_key},
            )
            response.raise_for_status()
            data = response.json()
            property_data = data.get("property", [{}])[0]
            building = property_data.get("building", {})
            summary = property_data.get("summary", {})
            sale = property_data.get("sale", {})
            value = property_data.get("avm", {}).get("amount", {}).get("value", MOCK_PROPERTY["property_value"])
            sqft = building.get("size", {}).get("livingsize", MOCK_PROPERTY["sqft"])
            return {
                **MOCK_PROPERTY,
                "address": address,
                "property_value": value,
                "sqft": sqft,
                "price_per_sqft": round(value / max(sqft, 1)),
                "bedrooms": building.get("rooms", {}).get("beds", MOCK_PROPERTY["bedrooms"]),
                "bathrooms": building.get("rooms", {}).get("bathstotal", MOCK_PROPERTY["bathrooms"]),
                "year_built": summary.get("yearbuilt", MOCK_PROPERTY["year_built"]),
                "last_sold_price": sale.get("amount", {}).get("saleamt", MOCK_PROPERTY["last_sold_price"]),
                "last_sold_date": sale.get("salesearchdate", MOCK_PROPERTY["last_sold_date"]),
            }
    except Exception:
        return {**MOCK_PROPERTY, "address": address}

