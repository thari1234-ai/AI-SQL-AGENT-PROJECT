export type ChartSpec = {
  type: "line" | "bar" | "pie" | "scatter" | "table";
  x_key?: string;
  y_key?: string;
  category_key?: string;
  value_key?: string;
};

export type ChatResponse = {
  prompt: string;
  sql: string;
  explanation: string;
  insight_summary: string;
  key_observations: string[];
  recommendations: string[];
  rows: Record<string, unknown>[];
  columns: string[];
  chart: ChartSpec;
  execution_ms: number;
  timestamp: string;
};
