import { NextResponse } from "next/server";

const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL ?? "http://localhost:8000";
const DEV_JWT_TOKEN = process.env.DEV_JWT_TOKEN ?? "";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const prompt = typeof body?.prompt === "string" ? body.prompt.trim() : "";

    if (!prompt) {
      return new NextResponse("Text is required", {
        status: 400,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    const res = await fetch(`${BACKEND_BASE_URL}/summarize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${DEV_JWT_TOKEN}`,
      },
      body: JSON.stringify({
        text: prompt,
        max_length: 100,
      }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const detail = data?.detail;
      const message =
        typeof detail === "string"
          ? detail
          : detail?.error ?? data?.error ?? "Backend request failed";
      return new NextResponse(message, {
        status: res.status,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    const summary = typeof data?.summary === "string" ? data.summary : "";
    return new NextResponse(summary, {
      status: 200,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Internal server error";
    return new NextResponse(message, {
      status: 500,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
}
