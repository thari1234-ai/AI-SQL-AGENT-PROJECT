"use client";

import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Database,
  MessageSquareText,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";

import { BrandLogo } from "@/components/ui/brand-logo";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const features = [
  { title: "Natural Language to SQL", desc: "Ask a question and receive accurate, structured SQL in seconds.", icon: MessageSquareText },
  { title: "Secure Query Guardrails", desc: "Only read-only analytics queries are allowed by default.", icon: ShieldCheck },
  { title: "Automatic Visuals", desc: "Results are transformed into appropriate charts instantly.", icon: BarChart3 },
  { title: "Schema-Aware Explorer", desc: "Understand tables, columns, and sample records at a glance.", icon: Database },
];

const howItWorks = [
  "Ask your data question in plain English.",
  "AI Agent generates safe SQL and validates it.",
  "You get table output, chart, and business summary.",
];

export default function LandingPage() {
  return (
    <main className="min-h-screen px-6 py-8 md:px-12">
      <section className="mx-auto flex max-w-6xl items-center justify-between pb-6">
        <BrandLogo />
        <div className="hidden items-center gap-6 text-sm text-slate-600 md:flex">
          <a href="#features" className="hover:text-slate-900">Features</a>
          <a href="#how" className="hover:text-slate-900">How it works</a>
          <a href="#faq" className="hover:text-slate-900">FAQ</a>
        </div>
      </section>

      <section className="mx-auto max-w-6xl">
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.45 }}>
          <Card className="overflow-hidden border-slate-300 p-8 md:p-14">
            <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Enterprise Analytics Platform</p>
            <h1 className="mt-4 max-w-4xl text-4xl font-bold leading-tight text-slate-950 md:text-6xl">AI SQL Agent</h1>
            <p className="mt-5 max-w-3xl text-base text-slate-600 md:text-lg">
              Ask questions in plain English. Instantly generate SQL, visualize data, and uncover insights from your database.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/login"><Button>Start Chatting <ArrowRight className="ml-2 h-4 w-4" /></Button></Link>
              <Link href="/dashboard"><Button variant="outline">View Demo</Button></Link>
            </div>

            <div className="mt-8 grid gap-3 md:grid-cols-3">
              {[
                "AI-generated SQL with explainability",
                "Read-only execution with safety filters",
                "Charts and insights in one response",
              ].map((item) => (
                <p key={item} className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-700">{item}</p>
              ))}
            </div>
          </Card>
        </motion.div>
      </section>

      <section id="features" className="mx-auto mt-12 grid max-w-6xl gap-4 md:grid-cols-2">
        {features.map((feature, idx) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.35, delay: idx * 0.04 }}
          >
            <Card className="h-full border-slate-200 p-6">
              <feature.icon className="h-5 w-5 text-slate-900" />
              <h3 className="mt-3 text-lg font-semibold text-slate-950">{feature.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{feature.desc}</p>
            </Card>
          </motion.div>
        ))}
      </section>

      <section id="how" className="mx-auto mt-12 max-w-6xl rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-2xl font-semibold text-slate-950">How it works</h2>
        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {howItWorks.map((step, index) => (
            <div key={step} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Step 0{index + 1}</p>
              <p className="mt-2 text-sm text-slate-700">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-12 max-w-6xl space-y-4">
        <h2 className="text-2xl font-semibold text-slate-950">Testimonials</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            "Our analysts deliver weekly insights in hours, not days.",
            "Security review passed faster because guardrails are built-in.",
            "Our leadership finally uses dashboards everyone understands.",
          ].map((quote) => (
            <Card key={quote} className="border-slate-200 p-5 text-sm text-slate-700">{quote}</Card>
          ))}
        </div>
      </section>

      <section id="faq" className="mx-auto mt-12 max-w-6xl space-y-3 pb-12">
        <h2 className="text-2xl font-semibold text-slate-950">FAQ</h2>
        {[
          ["Can I use my own PostgreSQL?", "Yes. Start with sample data, then connect your production database."],
          ["Does it block risky SQL?", "Yes. Non-read-only operations are blocked by default."],
          ["Can I export results?", "Yes. Export is available in CSV and XLSX formats."],
        ].map(([q, a]) => (
          <Card key={q} className="border-slate-200 p-5">
            <p className="font-semibold text-slate-950">{q}</p>
            <p className="mt-2 text-sm text-slate-600">{a}</p>
          </Card>
        ))}
      </section>

      <footer className="mx-auto mb-8 flex max-w-6xl flex-wrap items-center justify-between gap-3 border-t border-slate-200 pt-5 text-sm text-slate-500">
        <p>AI SQL Agent. Formal analytics workspace for teams.</p>
        <p className="inline-flex items-center gap-2"><Sparkles className="h-4 w-4" /> Built for clear, trusted decisions.</p>
      </footer>
    </main>
  );
}
