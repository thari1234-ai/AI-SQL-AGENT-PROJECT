import { ChatPanel } from "@/components/dashboard/chat-panel";

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<{ prompt?: string }>;
}) {
  const params = await searchParams;
  return <ChatPanel initialPrompt={params.prompt} />;
}
