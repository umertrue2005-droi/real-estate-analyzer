import os

import httpx

MOCK_WALKSCORE = {
    "walk_score": 78,
    "transit_score": 52,
    "bike_score": 61,
    "description": "Very Walkable",
}


async def get_scores(address: str) -> dict:
    api_key = os.getenv("WALKSCORE_API_KEY", "")
    if not api_key:
        return MOCK_WALKSCORE
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.walkscore.com/score",
                params={"format": "json", "address": address, "wsapikey": api_key, "transit": 1, "bike": 1},
            )
            response.raise_for_status()
            data = response.json()
            return {
                "walk_score": data.get("walkscore", MOCK_WALKSCORE["walk_score"]),
                "transit_score": data.get("transit", {}).get("score", MOCK_WALKSCORE["transit_score"]),
                "bike_score": data.get("bike", {}).get("score", MOCK_WALKSCORE["bike_score"]),
                "description": data.get("description", MOCK_WALKSCORE["description"]),
            }
    except Exception:
        return MOCK_WALKSCORE

