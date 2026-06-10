export type User = {
  id: number;
  name: string;
  email: string;
};

export type AgentStatus = "waiting" | "running" | "done" | "failed";

export type AgentLog = {
  name: string;
  status: AgentStatus;
  log: string;
  duration: number;
};

export type StatusResponse = {
  agents: AgentLog[];
  complete: boolean;
  address: string;
  status: string;
};

export type CompProperty = {
  address: string;
  price: number;
  sqft: number;
  price_per_sqft: number;
};

export type ResultsResponse = {
  id: number;
  address: string;
  market_data: {
    median_price: number;
    city_avg_price: number;
    price_per_sqft: number;
    subject_value: number;
    subject_vs_market_pct: number;
    trend_direction: string;
    comp_properties: CompProperty[];
    neighborhood_score: number;
    property: {
      property_value: number;
      zip_median_price: number;
      city_avg_price: number;
      price_per_sqft: number;
    };
  };
  financial_data: {
    cap_rate: number;
    cash_on_cash: number;
    GRM: number;
    break_even_occ: number;
    monthly_rent_est: number;
    annual_gross_rent: number;
    noi: number;
    annual_cash_flow: number;
    mortgage_payment: number;
    vacancy_rate: number;
  };
  zoning_data: {
    zone_code: string;
    zone_description: string;
    permitted_uses: string[];
    restrictions: string[];
    recent_permits: number;
    permit_backlog_days: number;
    development_potential: string;
  };
  risk_data: {
    risk_score: number;
    risk_level: string;
    walk_score: number;
    transit_score: number;
    bike_score: number;
    flood_zone: string;
    vacancy_rate: number;
    crime_index: number;
    risk_factors: string[];
  };
  report_data: {
    verdict: "Favorable" | "Proceed with Caution" | "High Risk";
    verdict_color: "green" | "amber" | "red";
    summary: string;
    memo_markdown: string;
    recommendation: string;
    confidence_score: number;
  };
};

export type ReportResponse = {
  memo_markdown: string;
  verdict: string;
  recommendation: string;
};

