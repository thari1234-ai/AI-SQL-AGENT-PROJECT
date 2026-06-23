import * as React from "react";

import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "ghost" | "outline";
};

export function Button({ className, variant = "default", ...props }: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold transition duration-200 active:scale-[0.99]";
  const variants = {
    default: "bg-slate-900 text-white shadow-[0_8px_24px_rgba(15,23,42,0.24)] hover:-translate-y-0.5 hover:bg-black",
    ghost: "text-slate-700 hover:bg-slate-100",
    outline: "border border-slate-300 bg-white text-slate-900 hover:border-slate-400 hover:bg-slate-50",
  };

  return <button className={cn(base, variants[variant], className)} {...props} />;
}
