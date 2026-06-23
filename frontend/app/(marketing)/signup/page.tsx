"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import axios from "axios";

import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SignupPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSignup() {
    setError("");
    if (!fullName.trim() || !email.trim() || !password.trim()) {
      setError("Please fill in all fields.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    try {
      setIsSubmitting(true);
      const { data } = await api.post<{ access_token: string }>("/auth/signup", { full_name: fullName, email, password });
      localStorage.setItem("token", data.access_token);
      router.push("/dashboard");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === "string") {
          setError(detail);
        } else if (Array.isArray(detail) && detail[0]?.msg) {
          setError(detail[0].msg);
        } else {
          setError("Could not create account");
        }
      } else {
        setError("Could not create account");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-b from-white to-slate-50 px-6">
      <Card className="w-full max-w-md space-y-4 border-slate-200 p-6">
        <h1 className="text-2xl font-semibold text-slate-950">Create your account</h1>
        <Input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Full name" autoComplete="name" />
        <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" autoComplete="email" />
        <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" autoComplete="new-password" />
        <p className="-mt-2 text-xs text-slate-500">Use at least 8 characters.</p>
        {error && <p className="text-sm text-rose-600">{error}</p>}
        <Button className="w-full" onClick={onSignup} disabled={isSubmitting}>{isSubmitting ? "Creating..." : "Create account"}</Button>
        <p className="text-sm text-slate-600">Already have an account? <Link href="/login" className="font-semibold text-slate-900">Log in</Link></p>
      </Card>
    </main>
  );
}
