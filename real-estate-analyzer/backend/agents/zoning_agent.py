from services.census_service import get_zoning


async def run_zoning_agent(address: str) -> dict:
    zoning = await get_zoning(address)
    return zoning

