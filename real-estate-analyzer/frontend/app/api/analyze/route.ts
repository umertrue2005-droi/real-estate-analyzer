import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json({ message: "Frontend calls the FastAPI backend directly at http://localhost:8000." }, { status: 501 });
}
