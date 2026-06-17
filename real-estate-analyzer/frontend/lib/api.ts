import type { ReportResponse, ResultsResponse, StatusResponse, User } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://real-estate-analyzer-production-6f73.up.railway.app";

type AuthResponse = {
  token: string;
  user: User;
};

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {})
    }
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }
  return (await response.json()) as T;
}

export function register(name: string, email: string, password: string): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password })
  });
}

export function login(email: string, password: string): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export function createAnalysis(address: string, token: string): Promise<{ analysis_id: number }> {
  return request<{ analysis_id: number }>("/api/analyze", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ address })
  });
}

export function getStatus(id: string, token: string): Promise<StatusResponse> {
  return request<StatusResponse>(`/api/analyze/${id}/status`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function getResults(id: string, token: string): Promise<ResultsResponse> {
  return request<ResultsResponse>(`/api/analyze/${id}/results`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function getReport(id: string, token: string): Promise<ReportResponse> {
  return request<ReportResponse>(`/api/analyze/${id}/report`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function saveReport(id: string, token: string): Promise<{ saved: boolean }> {
  return request<{ saved: boolean }>(`/api/analyze/${id}/save`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` }
  });
}
