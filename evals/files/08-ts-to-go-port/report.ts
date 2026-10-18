// report.ts — summarizes order events for the ops dashboard.
// CLI: node report.js < events.json   (compiled with tsc; output is consumed by a diffing job)
import { readFileSync } from "node:fs";

type Event = { user: string; amount: number; tags?: string[]; note?: string | null };
type Summary = {
  users: Record<string, { count: number; total: number; avg: number }>;
  amountsSorted: number[];
  longestNote: { user: string; chars: number } | null;
  tags: string[];
  half: number[];
};

export function summarize(events: Event[]): Summary {
  const users: Summary["users"] = {};
  const tags = new Set<string>();
  let longest: Summary["longestNote"] = null;
  for (const e of events) {
    const u = (users[e.user] ??= { count: 0, total: 0, avg: 0 });
    u.count += 1;
    u.total += e.amount;
    u.avg = u.total / u.count;
    for (const t of e.tags ?? []) tags.add(t);
    if (e.note && (longest === null || e.note.length > longest.chars)) {
      longest = { user: e.user, chars: e.note.length };
    }
  }
  return {
    users,
    amountsSorted: events.map((e) => e.amount).sort(),
    longestNote: longest,
    tags: [...tags],
    half: events.map((e) => Math.round(e.amount / 2)),
  };
}

if (require.main === module) {
  const events: Event[] = JSON.parse(readFileSync(0, "utf8"));
  console.log(JSON.stringify(summarize(events)));
}
