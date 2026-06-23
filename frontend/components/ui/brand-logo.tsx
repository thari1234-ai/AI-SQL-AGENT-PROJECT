import { DatabaseZap } from "lucide-react";
import Link from "next/link";

export function BrandLogo({ subtitle = true }: { subtitle?: boolean }) {
  return (
    <Link href="/landing" className="inline-flex items-center gap-3">
      <span className="grid h-9 w-9 place-items-center rounded-xl border border-slate-300 bg-slate-900 text-white">
        <DatabaseZap className="h-5 w-5" />
      </span>
      <span>
        <strong className="block text-sm leading-tight text-slate-900">AI SQL Agent</strong>
        {subtitle ? <span className="text-xs text-slate-500">Chat with Your Database</span> : null}
      </span>
    </Link>
  );
}
