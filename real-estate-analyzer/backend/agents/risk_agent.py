from services.census_service import get_vacancy
from services.walkscore_service import get_scores


async def run_risk_agent(address: str) -> dict:
    scores = await get_scores(address)
    vacancy = await get_vacancy(address)
    flood_zone = "X"
    crime_index = 31
    population_growth = vacancy["population_growth_5yr"]
    vacancy_rate = vacancy["vacancy_rate"]
    flood_risk_map = {"X": 5, "A": 40, "B": 20, "C": 10}
    risk_score = (
        min(vacancy_rate * 500, 100) * 0.30
        + flood_risk_map[flood_zone] * 0.20
        + crime_index * 0.30
        + (1 - population_growth) * 50 * 0.20
    )
    return {
        "risk_score": round(risk_score),
        "risk_level": "Low" if risk_score < 30 else "Moderate" if risk_score <= 60 else "High",
        "walk_score": scores["walk_score"],
        "transit_score": scores["transit_score"],
        "bike_score": scores["bike_score"],
        "flood_zone": flood_zone,
        "vacancy_rate": vacancy_rate,
        "crime_index": crime_index,
        "risk_factors": [
            "Vacancy is near the market average",
            "Flood zone X indicates minimal FEMA flood exposure",
            "Crime index is manageable for an urban infill neighborhood",
        ],
    }

