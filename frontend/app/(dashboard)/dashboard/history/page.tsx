"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";

type HistoryItem = {
  id: number;
  prompt: string;
  sql_text: string;
  execution_ms: number;
  created_at: string;
};

export default function HistoryPage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["history"],
    queryFn: async () => (await api.get<HistoryItem[]>("/history")).data,
    retry: false,
  });

  const authError = axios.isAxiosError(error) && error.response?.status === 401;

  return (
    <Card className="border-slate-200 p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h2 className="text-lg font-semibold text-slate-950">Query History</h2>
        <Button variant="outline" onClick={() => refetch()}>Refresh</Button>
      </div>

      {isLoading ? <p className="text-sm text-slate-600">Loading history...</p> : null}
      {authError ? (
        <div className="space-y-2 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
          <p>You are not logged in. Please sign in to view query history.</p>
          <Link href="/login" className="inline-block rounded-lg border border-amber-300 bg-white px-3 py-1 font-medium text-amber-900 hover:bg-amber-100">
            Go to login
          </Link>
        </div>
      ) : null}

      {!isLoading && !error && (data ?? []).length === 0 ? (
        <p className="text-sm text-slate-600">No history yet. Run a query from Chat to populate this page.</p>
      ) : null}

      <div className="space-y-2">
        {(data ?? []).map((item) => (
          <div key={item.id} className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm">
            <p className="font-semibold text-slate-900">{item.prompt}</p>
            <p className="mt-1 text-slate-600">{item.sql_text}</p>
            <p className="mt-1 text-xs text-slate-500">{item.execution_ms} ms</p>
            <div className="mt-2 flex flex-wrap gap-2">
              <Link href={`/dashboard?prompt=${encodeURIComponent(item.prompt)}`} className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs font-medium text-slate-800 hover:bg-slate-100">
                Re-run
              </Link>
              <a href={`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}/history/${item.id}/export/csv`} className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs font-medium text-slate-800 hover:bg-slate-100">
                Export CSV
              </a>
              <a href={`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}/history/${item.id}/export/xlsx`} className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs font-medium text-slate-800 hover:bg-slate-100">
                Export XLSX
              </a>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
