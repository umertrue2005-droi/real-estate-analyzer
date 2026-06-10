import os
import re

import httpx

MOCK_DEMOGRAPHICS = {
    "median_household_income": 68400,
    "population": 24800,
    "population_growth_5yr": 0.12,
    "vacancy_rate": 0.068,
    "owner_occupied_pct": 0.54,
    "median_age": 34.2,
    "unemployment_rate": 0.038,
}

MOCK_ZONING = {
    "zone_code": "R2",
    "zone_description": "Medium density residential district",
    "permitted_uses": ["Single Family", "Duplex", "ADU"],
    "restrictions": ["Max 35ft height", "Min 5ft setback"],
    "recent_permits": 3,
    "permit_backlog_days": 45,
    "development_potential": "ADU or duplex conversion appears feasible subject to local review.",
}


def extract_zip(address: str) -> str:
    match = re.search(r"\b\d{5}\b", address)
    return match.group(0) if match else "78702"


async def get_demographics(address: str) -> dict:
    api_key = os.getenv("CENSUS_API_KEY", "")
    if not api_key:
        return MOCK_DEMOGRAPHICS
    try:
        zip_code = extract_zip(address)
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.census.gov/data/2022/acs/acs5",
                params={
                    "get": "B19013_001E,B01003_001E,B25004_001E,B25003_002E,B01002_001E,B23025_005E",
                    "for": f"zip code tabulation area:{zip_code}",
                    "key": api_key,
                },
            )
            response.raise_for_status()
            rows = response.json()
            if len(rows) < 2:
                return MOCK_DEMOGRAPHICS
            values = rows[1]
            return {
                **MOCK_DEMOGRAPHICS,
                "median_household_income": int(values[0]),
                "population": int(values[1]),
                "median_age": float(values[4]),
            }
    except Exception:
        return MOCK_DEMOGRAPHICS


async def get_zoning(address: str) -> dict:
    return MOCK_ZONING


async def get_vacancy(address: str) -> dict:
    demographics = await get_demographics(address)
    return {"vacancy_rate": demographics["vacancy_rate"], "population_growth_5yr": demographics["population_growth_5yr"]}

