"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

type Dashboard = {
  id: number;
  name: string;
  created_at: string;
};

export default function DashboardsPage() {
  const queryClient = useQueryClient();
  const [name, setName] = useState("Executive Snapshot");
  const [message, setMessage] = useState("");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["dashboards"],
    queryFn: async () => (await api.get<Dashboard[]>("/dashboards")).data,
    retry: false,
  });

  const createMutation = useMutation({
    mutationFn: async (dashboardName: string) => (await api.post<Dashboard>("/dashboards", { name: dashboardName })).data,
    onSuccess: () => {
      setMessage("Dashboard created.");
      queryClient.invalidateQueries({ queryKey: ["dashboards"] });
    },
  });

  const authError = axios.isAxiosError(error) && error.response?.status === 401;

  function createDashboard() {
    if (!name.trim()) {
      setMessage("Please enter a dashboard name.");
      return;
    }
    setMessage("");
    createMutation.mutate(name);
  }

  return (
    <Card className="border-slate-200 p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h2 className="text-lg font-semibold text-slate-950">Saved Dashboards</h2>
        <Button variant="outline" onClick={() => refetch()}>Refresh</Button>
      </div>

      {authError ? (
        <div className="space-y-2 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
          <p>You are not logged in. Please sign in to manage dashboards.</p>
          <Link href="/login" className="inline-block rounded-lg border border-amber-300 bg-white px-3 py-1 font-medium text-amber-900 hover:bg-amber-100">
            Go to login
          </Link>
        </div>
      ) : (
        <>
          <p className="text-sm text-slate-600">Create and manage saved dashboard workspaces.</p>

          <div className="mt-3 flex flex-wrap gap-2">
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Dashboard name" className="max-w-sm" />
            <Button onClick={createDashboard} disabled={createMutation.isPending}>
              {createMutation.isPending ? "Creating..." : "Create dashboard"}
            </Button>
          </div>

          {message ? <p className="mt-2 text-sm text-slate-700">{message}</p> : null}
          {isLoading ? <p className="mt-2 text-sm text-slate-600">Loading dashboards...</p> : null}

          <div className="mt-3 space-y-2">
            {(data ?? []).map((dashboard) => (
              <div key={dashboard.id} className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-800">
                <p className="font-semibold">{dashboard.name}</p>
                <p className="text-xs text-slate-500">ID: {dashboard.id}</p>
              </div>
            ))}
            {!isLoading && (data ?? []).length === 0 ? (
              <p className="text-sm text-slate-600">No dashboards yet. Create your first one above.</p>
            ) : null}
          </div>
        </>
      )}
    </Card>
  );
}
