import os

import httpx

MOCK_RENT = {
    "rent_estimate": 2850,
    "rent_range_low": 2600,
    "rent_range_high": 3100,
    "vacancy_rate": 0.07,
    "price_to_rent_ratio": 12.4,
}


async def get_rent_estimate(address: str, bedrooms: int = 3, bathrooms: int = 2) -> dict:
    api_key = os.getenv("RENTCAST_API_KEY", "")
    if not api_key:
        return MOCK_RENT
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.rentcast.io/v1/avm/rent/long-term",
                params={"address": address, "bedrooms": bedrooms, "bathrooms": bathrooms},
                headers={"X-Api-Key": api_key},
            )
            response.raise_for_status()
            data = response.json()
            return {
                **MOCK_RENT,
                "rent_estimate": data.get("rent", MOCK_RENT["rent_estimate"]),
                "rent_range_low": data.get("rentRangeLow", MOCK_RENT["rent_range_low"]),
                "rent_range_high": data.get("rentRangeHigh", MOCK_RENT["rent_range_high"]),
            }
    except Exception:
        return MOCK_RENT

