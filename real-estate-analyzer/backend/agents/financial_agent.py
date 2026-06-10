from services.attom_service import get_property_detail
from services.rentcast_service import get_rent_estimate


def monthly_mortgage(principal: float, annual_rate: float = 0.07, years: int = 30) -> float:
    rate = annual_rate / 12
    months = years * 12
    return principal * (rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)


async def run_financial_agent(address: str) -> dict:
    property_detail = await get_property_detail(address)
    rent = await get_rent_estimate(address, property_detail["bedrooms"], property_detail["bathrooms"])
    property_value = property_detail["property_value"]
    monthly_rent = rent["rent_estimate"]
    annual_gross_rent = monthly_rent * 12
    operating_expenses = annual_gross_rent * 0.35
    noi = annual_gross_rent - operating_expenses
    mortgage_payment = monthly_mortgage(property_value * 0.75)
    annual_cash_flow = noi - (mortgage_payment * 12)
    cash_invested = property_value * 0.25
    return {
        "cap_rate": round(noi / property_value * 100, 1),
        "cash_on_cash": round(annual_cash_flow / cash_invested * 100, 1),
        "GRM": round(property_value / (monthly_rent * 12), 1),
        "break_even_occ": round(operating_expenses / annual_gross_rent * 100, 1),
        "monthly_rent_est": monthly_rent,
        "annual_gross_rent": annual_gross_rent,
        "noi": round(noi),
        "annual_cash_flow": round(annual_cash_flow),
        "mortgage_payment": round(mortgage_payment),
        "rent_range_low": rent["rent_range_low"],
        "rent_range_high": rent["rent_range_high"],
        "vacancy_rate": rent["vacancy_rate"],
    }
