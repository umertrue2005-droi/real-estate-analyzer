import os

import httpx

from services.gemini_service import generate_text, parse_json_object

DEFAULT_PROPERTY = {
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
    "comps": [],
}


def _address_seed(address: str) -> int:
    return sum((index + 1) * ord(char) for index, char in enumerate(address))


def address_based_property_estimate(address: str) -> dict:
    seed = _address_seed(address)
    sqft = 1200 + seed % 1800
    price_per_sqft = 170 + seed % 310
    property_value = sqft * price_per_sqft
    zip_median_price = round(property_value * (0.9 + (seed % 25) / 100))
    comps = []
    for index, multiplier in enumerate((0.94, 1.01, 1.08), start=1):
        comp_sqft = round(sqft * (0.92 + ((seed + index * 7) % 18) / 100))
        comp_price = round(property_value * multiplier)
        comps.append(
            {
                "address": f"Comparable {index} near {address}",
                "price": comp_price,
                "sqft": comp_sqft,
                "price_per_sqft": round(comp_price / max(comp_sqft, 1)),
            }
        )
    return {
        **DEFAULT_PROPERTY,
        "address": address,
        "property_value": round(property_value),
        "price_per_sqft": price_per_sqft,
        "bedrooms": 2 + seed % 4,
        "bathrooms": 1 + (seed % 3),
        "sqft": sqft,
        "year_built": 1950 + seed % 70,
        "last_sold_price": round(property_value * 0.88),
        "zip_median_price": zip_median_price,
        "city_avg_price": round(zip_median_price * 1.04),
        "comps": comps,
        "estimate_source": "address_based_fallback",
    }


async def get_gemini_property_detail(address: str) -> dict:
    prompt = f"""
You are a US residential real estate valuation analyst.
Estimate realistic property details for this address: {address}

Use the address, city, state, ZIP, and your knowledge of US housing markets to produce address-specific estimates.
Return only valid JSON with these exact keys:
property_value, price_per_sqft, bedrooms, bathrooms, sqft, year_built, last_sold_price,
last_sold_date, zip_median_price, city_avg_price, comps.

comps must be an array of 3 nearby comparable homes, each with address, price, sqft, price_per_sqft.
All money and sqft fields must be integers. bathrooms may be a number. last_sold_date must be YYYY-MM-DD.
Do not use placeholder Austin data unless the requested address is actually in Austin.
"""
    try:
        data = parse_json_object(await generate_text(prompt))
        fallback = address_based_property_estimate(address)
        value = int(data.get("property_value") or fallback["property_value"])
        sqft = int(data.get("sqft") or fallback["sqft"])
        comps = data.get("comps") if isinstance(data.get("comps"), list) else fallback["comps"]
        return {
            **fallback,
            "address": address,
            "property_value": value,
            "price_per_sqft": int(data.get("price_per_sqft") or round(value / max(sqft, 1))),
            "bedrooms": int(data.get("bedrooms") or fallback["bedrooms"]),
            "bathrooms": float(data.get("bathrooms") or fallback["bathrooms"]),
            "sqft": sqft,
            "year_built": int(data.get("year_built") or fallback["year_built"]),
            "last_sold_price": int(data.get("last_sold_price") or fallback["last_sold_price"]),
            "last_sold_date": data.get("last_sold_date") or fallback["last_sold_date"],
            "zip_median_price": int(data.get("zip_median_price") or fallback["zip_median_price"]),
            "city_avg_price": int(data.get("city_avg_price") or fallback["city_avg_price"]),
            "comps": comps[:3],
            "estimate_source": "gemini",
        }
    except Exception:
        return address_based_property_estimate(address)


async def get_property_detail(address: str) -> dict:
    api_key = os.getenv("ATTOM_API_KEY", "")
    if not api_key:
        return await get_gemini_property_detail(address)
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
            fallback = address_based_property_estimate(address)
            value = property_data.get("avm", {}).get("amount", {}).get("value", fallback["property_value"])
            sqft = building.get("size", {}).get("livingsize", fallback["sqft"])
            return {
                **fallback,
                "address": address,
                "property_value": value,
                "sqft": sqft,
                "price_per_sqft": round(value / max(sqft, 1)),
                "bedrooms": building.get("rooms", {}).get("beds", fallback["bedrooms"]),
                "bathrooms": building.get("rooms", {}).get("bathstotal", fallback["bathrooms"]),
                "year_built": summary.get("yearbuilt", fallback["year_built"]),
                "last_sold_price": sale.get("amount", {}).get("saleamt", fallback["last_sold_price"]),
                "last_sold_date": sale.get("salesearchdate", fallback["last_sold_date"]),
                "estimate_source": "attom",
            }
    except Exception:
        return await get_gemini_property_detail(address)
