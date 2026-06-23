"use client";

import ReactECharts from "echarts-for-react";

import type { ChartSpec } from "@/types/chat";

export function ResultChart({ rows, chart }: { rows: Record<string, unknown>[]; chart: ChartSpec }) {
  if (!rows.length || chart.type === "table") return null;

  if (chart.type === "bar" || chart.type === "line") {
    const x = rows.map((r) => String(r[chart.x_key ?? ""] ?? ""));
    const y = rows.map((r) => Number(r[chart.y_key ?? ""] ?? 0));
    return (
      <ReactECharts
        style={{ height: 300 }}
        option={{
          xAxis: { type: "category", data: x },
          yAxis: { type: "value" },
          series: [{ type: chart.type, data: y, smooth: chart.type === "line" }],
          grid: { left: 30, right: 20, top: 30, bottom: 30 },
          tooltip: { trigger: "axis" },
        }}
      />
    );
  }

  if (chart.type === "pie") {
    const pieData = rows.map((r) => ({
      name: String(r[chart.category_key ?? ""] ?? ""),
      value: Number(r[chart.value_key ?? ""] ?? 0),
    }));

    return <ReactECharts style={{ height: 300 }} option={{ tooltip: { trigger: "item" }, series: [{ type: "pie", data: pieData }] }} />;
  }

  if (chart.type === "scatter") {
    const data = rows.map((r) => [Number(r[chart.x_key ?? ""] ?? 0), Number(r[chart.y_key ?? ""] ?? 0)]);
    return <ReactECharts style={{ height: 300 }} option={{ xAxis: {}, yAxis: {}, series: [{ type: "scatter", data }] }} />;
  }

  return null;
}
