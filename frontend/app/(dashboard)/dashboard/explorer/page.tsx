"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function ExplorerPage() {
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [tableName, setTableName] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["tables"],
    queryFn: async () => (await api.get<{ table_name: string }[]>("/explorer/tables")).data,
    retry: false,
  });

  const detailsQuery = useQuery({
    queryKey: ["table-details", selectedTable],
    queryFn: async () => (await api.get<{ row_count: number; columns: { column_name: string; data_type: string }[] }>(`/explorer/tables/${selectedTable}`)).data,
    enabled: Boolean(selectedTable),
    retry: false,
  });

  const authError = axios.isAxiosError(error) && error.response?.status === 401;

  async function uploadDataset() {
    if (!uploadFile) {
      setUploadMessage("Select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadFile);
    if (tableName.trim()) {
      formData.append("table_name", tableName.trim());
    }

    setIsUploading(true);
    setUploadMessage("");
    try {
      const { data: result } = await api.post<{ table_name: string; row_count: number }>("/explorer/upload", formData);
      setUploadMessage(`Imported ${result.row_count} rows into table ${result.table_name}.`);
      setSelectedTable(result.table_name);
      await refetch();
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setUploadMessage(err.response?.data?.detail ?? "Upload failed.");
      } else {
        setUploadMessage("Upload failed.");
      }
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="space-y-5">
      <Card className="relative overflow-hidden border-slate-200 bg-white p-5 md:p-7">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-r from-slate-100 via-white to-slate-100" />
        <div className="relative mx-auto max-w-3xl space-y-5">
          <div className="text-center">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-950">Upload Data</h2>
            <p className="mt-1 text-sm text-slate-600">Drop in your CSV, XLSX, or JSON file and start querying instantly.</p>
          </div>

          {authError ? (
            <div className="space-y-2 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
              <p>You are not logged in. Please sign in to explore and upload tables.</p>
              <Link href="/login" className="inline-block rounded-lg border border-amber-300 bg-white px-3 py-1.5 font-medium text-amber-900 hover:bg-amber-100">
                Go to login
              </Link>
            </div>
          ) : (
            <div className="space-y-3 rounded-2xl border border-slate-200 bg-slate-50/70 p-4 md:p-5">
              <Input
                value={tableName}
                onChange={(e) => setTableName(e.target.value)}
                placeholder="Optional table name"
                className="h-11 border-slate-300 bg-white"
              />
              <div className="flex flex-col items-stretch gap-3 md:flex-row">
                <input
                  type="file"
                  accept=".csv,.xlsx,.xlsm,.json"
                  onChange={(e) => setUploadFile(e.target.files?.[0] ?? null)}
                  className="h-11 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm"
                />
                <Button onClick={uploadDataset} disabled={isUploading} className="h-11 px-6 md:min-w-36">
                  {isUploading ? "Uploading..." : "Upload Data"}
                </Button>
              </div>
              {uploadMessage ? (
                <p className="rounded-lg bg-white px-3 py-2 text-sm text-slate-700">{uploadMessage}</p>
              ) : null}
            </div>
          )}
        </div>
      </Card>

      <Card className="border-slate-200 bg-white p-4 md:p-5">
        <div className="mb-3 flex items-center justify-between gap-2">
          <h3 className="text-lg font-semibold text-slate-950">Data Explorer</h3>
          <Button variant="outline" onClick={() => refetch()}>
            Refresh
          </Button>
        </div>

        {isLoading ? <p className="text-sm text-slate-600">Loading tables...</p> : null}
        {isLoading ? <p className="text-xs text-slate-500">If this takes more than a few seconds, click Refresh.</p> : null}

        <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {(data ?? []).map((table) => (
            <button
              key={table.table_name}
              onClick={() => setSelectedTable(table.table_name)}
              className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-left text-sm text-slate-700 transition hover:bg-white"
            >
              {table.table_name}
            </button>
          ))}
        </div>

        {selectedTable ? (
          <div className="mt-4 rounded-xl border border-slate-200 bg-white p-3">
            <h4 className="text-sm font-semibold text-slate-900">Table: {selectedTable}</h4>
            {detailsQuery.isLoading ? <p className="mt-2 text-sm text-slate-600">Loading details...</p> : null}
            {!detailsQuery.isLoading && detailsQuery.data ? (
              <div className="mt-2 space-y-2 text-sm text-slate-700">
                <p>Rows: {detailsQuery.data.row_count}</p>
                <div className="grid gap-2 sm:grid-cols-2">
                  {detailsQuery.data.columns.map((column) => (
                    <div key={column.column_name} className="rounded-lg border border-slate-200 bg-slate-50 px-2 py-1">
                      {column.column_name} <span className="text-slate-500">({column.data_type})</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        ) : null}
      </Card>
    </div>
  );
}
