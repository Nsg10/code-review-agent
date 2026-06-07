export function parseAgentResult(raw) {
  const result = { score: null, summary: null, sections: [] };

  const scoreMatch = raw.match(/(?:SCORE|PERFORMANCE_SCORE|ARCHITECTURE_SCORE|SEVERITY):\s*(.+)/i);
  if (scoreMatch) {
    const val = scoreMatch[1].trim();
    const num = parseInt(val);
    result.score = isNaN(num) ? val : num;
  }

  const summaryMatch = raw.match(/SUMMARY:\s*([\s\S]+?)(?=\n[A-Z][A-Z_]+:|$)/);
  if (summaryMatch) {
    result.summary = summaryMatch[1].trim();
  }

  const sectionRegex = /([A-Z][A-Z_ ]+):\s*\n([\s\S]+?)(?=\n[A-Z][A-Z_ ]+:|$)/g;
  let match;
  while ((match = sectionRegex.exec(raw)) !== null) {
    const name = match[1].trim();
    if (name === "SUMMARY") continue;
    const content = match[2].trim();
    const items = content
      .split("\n")
      .map((l) => l.trim())
      .filter((l) => l.startsWith("-"))
      .map((l) => l.replace(/^-\s*/, "").replace(/\*\*/g, ""));
    if (items.length > 0) {
      result.sections.push({ title: formatTitle(name), items });
    }
  }

  return result;
}

function formatTitle(key) {
  return key.replace(/_/g, " ").toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
}