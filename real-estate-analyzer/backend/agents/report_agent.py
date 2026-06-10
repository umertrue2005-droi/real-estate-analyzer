import os

from openai import AsyncOpenAI


def fallback_report(market: dict, financial: dict, zoning: dict, risk: dict) -> dict:
    verdict = "Favorable" if financial["cap_rate"] > 5 and risk["risk_score"] < 45 else "Proceed with Caution"
    recommendation = "Buy with disciplined underwriting" if verdict == "Favorable" else "Negotiate price or improve financing terms"
    memo = f"""# Investment Memo

## Executive Summary

Verdict: **{verdict}**. The subject property is valued at ${market["subject_value"]:,} with a {financial["cap_rate"]}% cap rate and {financial["cash_on_cash"]}% cash-on-cash return. Risk is measured at {risk["risk_score"]}/100, supported by walkability and manageable vacancy exposure.

## Market Analysis

The property trades at ${market["price_per_sqft"]}/sqft compared with a ZIP median price of ${market["median_price"]:,}. Comparable sales cluster between ${min(c["price"] for c in market["comp_properties"]):,} and ${max(c["price"] for c in market["comp_properties"]):,}, placing the asset close to market value. Neighborhood fundamentals are {market["trend_direction"].lower()} with a neighborhood score of {market["neighborhood_score"]}/100.

## Financial Model

Estimated monthly rent is ${financial["monthly_rent_est"]:,}, or ${financial["annual_gross_rent"]:,} annually. NOI is approximately ${financial["noi"]:,}, producing a {financial["cap_rate"]}% cap rate, {financial["cash_on_cash"]}% cash-on-cash return, {financial["GRM"]} GRM, and {financial["break_even_occ"]}% break-even occupancy.

## Zoning & Legal

The parcel is classified as {zoning["zone_code"]}: {zoning["zone_description"]}. Permitted uses include {", ".join(zoning["permitted_uses"])}. Recent permit activity is {zoning["recent_permits"]} permits with an estimated {zoning["permit_backlog_days"]}-day backlog.

## Risk Assessment

Composite risk is {risk["risk_score"]}/100 ({risk["risk_level"]}). Walk Score is {risk["walk_score"]}, Transit Score is {risk["transit_score"]}, flood zone is {risk["flood_zone"]}, vacancy is {risk["vacancy_rate"] * 100:.1f}%, and crime index is {risk["crime_index"]}/100.

## Recommendation

{recommendation}. Prioritize rent verification, insurance review, and zoning confirmation before closing.
"""
    return {
        "verdict": verdict,
        "verdict_color": "green" if verdict == "Favorable" else "amber",
        "summary": f"{verdict}: {financial['cap_rate']}% cap rate with {risk['risk_score']}/100 risk.",
        "memo_markdown": memo,
        "recommendation": recommendation,
        "confidence_score": 86,
    }


async def run_report_agent(market: dict, financial: dict, zoning: dict, risk: dict) -> dict:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return fallback_report(market, financial, zoning, risk)
    try:
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior real estate investment analyst. Write a professional markdown investment memo with Executive Summary, Market Analysis, Financial Model, Zoning & Legal, Risk Assessment, and Recommendation. Be specific with numbers. Be direct.",
                },
                {"role": "user", "content": str({"market": market, "financial": financial, "zoning": zoning, "risk": risk})},
            ],
            temperature=0.2,
        )
        fallback = fallback_report(market, financial, zoning, risk)
        fallback["memo_markdown"] = response.choices[0].message.content or fallback["memo_markdown"]
        return fallback
    except Exception:
        return fallback_report(market, financial, zoning, risk)

