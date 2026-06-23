"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import axios from "axios";

import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onLogin() {
    setError("");
    if (!email.trim() || !password.trim()) {
      setError("Please enter email and password.");
      return;
    }

    try {
      setIsSubmitting(true);
      const { data } = await api.post<{ access_token: string }>("/auth/login", { email, password });
      localStorage.setItem("token", data.access_token);
      router.push("/dashboard");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === "string") {
          setError(detail);
        } else {
          setError("Invalid credentials");
        }
      } else {
        setError("Invalid credentials");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-b from-white to-slate-50 px-6">
      <Card className="w-full max-w-md space-y-4 border-slate-200 p-6">
        <h1 className="text-2xl font-semibold text-slate-950">Welcome back</h1>
        <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" autoComplete="email" />
        <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" autoComplete="current-password" />
        {error && <p className="text-sm text-rose-600">{error}</p>}
        <Button className="w-full" onClick={onLogin} disabled={isSubmitting}>{isSubmitting ? "Signing in..." : "Login"}</Button>
        <p className="text-sm text-slate-600">No account? <Link href="/signup" className="font-semibold text-slate-900">Create one</Link></p>
      </Card>
    </main>
  );
}
