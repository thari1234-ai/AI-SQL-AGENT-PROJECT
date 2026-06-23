"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SettingsPage() {
  const router = useRouter();
  const [workspaceLabel, setWorkspaceLabel] = useState("My Workspace");
  const [defaultPrompt, setDefaultPrompt] = useState("Show monthly revenue by region.");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const name = localStorage.getItem("workspace-label");
    const prompt = localStorage.getItem("default-prompt");
    if (name) setWorkspaceLabel(name);
    if (prompt) setDefaultPrompt(prompt);
  }, []);

  function save() {
    localStorage.setItem("workspace-label", workspaceLabel);
    localStorage.setItem("default-prompt", defaultPrompt);
    setSaved(true);
    setTimeout(() => setSaved(false), 1400);
  }

  function logout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  return (
    <Card className="space-y-4 border-slate-200 p-4">
      <h2 className="text-lg font-semibold text-slate-950">Settings</h2>

      <div className="space-y-2">
        <p className="text-sm font-medium text-slate-800">Workspace label</p>
        <Input value={workspaceLabel} onChange={(e) => setWorkspaceLabel(e.target.value)} placeholder="Workspace name" />
      </div>

      <div className="space-y-2">
        <p className="text-sm font-medium text-slate-800">Default chat prompt</p>
        <Input value={defaultPrompt} onChange={(e) => setDefaultPrompt(e.target.value)} placeholder="Default prompt" />
      </div>

      <div className="flex flex-wrap gap-2">
        <Button onClick={save}>Save settings</Button>
        <Button variant="outline" onClick={() => router.push("/login")}>Go to login</Button>
        <Button variant="outline" onClick={logout}>Logout</Button>
      </div>

      {saved ? <p className="text-sm text-emerald-700">Settings saved.</p> : null}
    </Card>
  );
}
