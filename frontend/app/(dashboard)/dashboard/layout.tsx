"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { cn } from "@/lib/utils";

import { BrandLogo } from "@/components/ui/brand-logo";

const nav = [
  { href: "/dashboard", label: "Chat" },
  { href: "/dashboard/history", label: "Query History" },
  { href: "/dashboard/dashboards", label: "Saved Dashboards" },
  { href: "/dashboard/explorer", label: "Data Explorer" },
  { href: "/dashboard/settings", label: "Settings" },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    localStorage.removeItem("ui-theme");
    document.documentElement.removeAttribute("data-theme");
  }, []);

  function logout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  return (
    <div className="grid min-h-screen grid-cols-1 bg-white md:grid-cols-[260px_1fr]">
      <aside className="border-r border-slate-200 bg-slate-50/70 p-4">
        <div className="mb-4"><BrandLogo subtitle={false} /></div>
        <nav className="space-y-2">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "block rounded-xl px-3 py-2 text-sm transition",
                pathname === item.href
                  ? "bg-white text-slate-950 shadow-[0_4px_12px_rgba(15,23,42,0.08)]"
                  : "text-slate-700 hover:bg-white hover:text-slate-950",
              )}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <section className="p-4 md:p-6">
        <header className="mb-4 flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-3 shadow-[0_6px_24px_rgba(15,23,42,0.06)]">
          <p className="text-sm text-slate-700">Data Source: Your uploaded tables</p>
          <div className="flex items-center gap-3 text-sm text-slate-600">
            <button
              onClick={() => router.push("/dashboard/settings")}
              className="rounded-lg border border-slate-300 px-2 py-1 hover:bg-slate-50"
            >
              User
            </button>
            <button onClick={logout} className="rounded-lg border border-slate-300 px-2 py-1 hover:bg-slate-50">Logout</button>
          </div>
        </header>
        {children}
      </section>
    </div>
  );
}
