"use client";

import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import Link from "next/link";
import { useEffect, useState } from "react";

import { api } from "@/lib/api";
import type { ChatResponse } from "@/types/chat";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

import { ResultChart } from "./result-chart";
import { ResultTable } from "./result-table";

function buildFallbackResponse(prompt: string): ChatResponse {
  const lower = prompt.toLowerCase();

  if (lower.includes("monthly") && lower.includes("revenue") && lower.includes("region")) {
    const rows = [
      { month: "2025-01", region: "North", total_revenue: 124500 },
      { month: "2025-01", region: "South", total_revenue: 139200 },
      { month: "2025-02", region: "North", total_revenue: 132800 },
      { month: "2025-02", region: "South", total_revenue: 146400 },
      { month: "2025-03", region: "North", total_revenue: 141300 },
      { month: "2025-03", region: "South", total_revenue: 153900 },
    ];

    return {
      prompt,
      sql: "SELECT DATE_TRUNC('month', order_date) AS month, region, SUM(revenue) AS total_revenue FROM sales GROUP BY 1, 2 ORDER BY 1, 2",
      explanation: "Generated a safe read-only SQL query and grouped results by month and region.",
      insight_summary: "Revenue increased month-over-month, with the South region consistently leading growth.",
      key_observations: [
        "South region revenue is higher than North across all displayed months.",
        "Both regions show a positive trend from January to March.",
      ],
      recommendations: [
        "Compare product mix in South vs North to replicate winning strategy.",
        "Set regional monthly targets based on March uplift trajectory.",
      ],
      rows,
      columns: ["month", "region", "total_revenue"],
      chart: { type: "bar", x_key: "month", y_key: "total_revenue" },
      execution_ms: 42,
      timestamp: new Date().toISOString(),
    };
  }

  const rows = [
    { label: "Sample A", value: 120 },
    { label: "Sample B", value: 98 },
    { label: "Sample C", value: 143 },
  ];

  return {
    prompt,
    sql: "SELECT label, value FROM sample_metrics ORDER BY value DESC LIMIT 50",
    explanation: "Backend is unavailable, so this is a local demo result to keep the UI interactive.",
    insight_summary: "Sample C is currently the top performer in this fallback dataset.",
    key_observations: ["Sample C leads by a notable margin.", "Distribution is moderately spread across categories."],
    recommendations: ["Reconnect backend to run against your real database."],
    rows,
    columns: ["label", "value"],
    chart: { type: "bar", x_key: "label", y_key: "value" },
    execution_ms: 1,
    timestamp: new Date().toISOString(),
  };
}

export function ChatPanel({ initialPrompt }: { initialPrompt?: string }) {
  const [prompt, setPrompt] = useState(initialPrompt ?? "Show monthly revenue by region.");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [mode, setMode] = useState<"live" | "fallback" | null>(null);
  const [error, setError] = useState("");
  const [hasSession, setHasSession] = useState(false);

  const mutation = useMutation({
    mutationFn: async (message: string) => {
      setError("");
      try {
        const { data } = await api.post<ChatResponse>("/chat", { prompt: message });
        setMode("live");
        return data;
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          setError("Your session has expired. Please log in again.");
          throw err;
        }

        setMode("fallback");
        setError("Live API is unavailable. Showing local demo result.");
        return buildFallbackResponse(message);
      }
    },
    onSuccess: (data) => setResponse(data),
  });

  useEffect(() => {
    if (initialPrompt) {
      setPrompt(initialPrompt);
      return;
    }
    const savedPrompt = localStorage.getItem("default-prompt");
    if (savedPrompt) {
      setPrompt(savedPrompt);
    }

    setHasSession(Boolean(localStorage.getItem("token")));
  }, [initialPrompt]);

  function runPrompt() {
    if (!prompt.trim()) {
      setError("Please enter a question before running.");
      return;
    }
    mutation.mutate(prompt);
  }

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="mb-3 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
          Upload data first from <Link href="/dashboard/explorer" className="font-semibold underline">Data Explorer</Link>, then ask questions here.
        </div>
        {!hasSession ? (
          <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
            You are in demo mode. <Link href="/login" className="font-semibold underline">Log in</Link> to run live queries.
          </div>
        ) : null}
        <form
          className="flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            runPrompt();
          }}
        >
          <Input value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Ask about your data..." />
          <Button type="submit" disabled={mutation.isPending}>{mutation.isPending ? "Running..." : "Run"}</Button>
        </form>
        {error ? <p className="mt-2 text-sm text-amber-700">{error}</p> : null}
      </Card>

      {response && (
        <Card className="space-y-4 p-4">
          <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
            Source: {mode === "live" ? "Live API" : "Local demo fallback"}
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">AI Explanation</p>
            <p className="text-sm text-slate-700">{response.explanation}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">Generated SQL</p>
            <pre className="overflow-auto rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700">{response.sql}</pre>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">Business Insight</p>
            <p className="text-sm text-slate-700">{response.insight_summary}</p>
          </div>
          <ResultChart rows={response.rows} chart={response.chart} />
          <ResultTable columns={response.columns} rows={response.rows} />
        </Card>
      )}
    </div>
  );
}
