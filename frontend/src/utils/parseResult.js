export function parseAgentResult(raw) {
  const result = { score: null, summary: null, sections: [] };
  const scoreMatch = raw.match(/(?:SCORE|PERFORMANCE_SCORE|ARCHITECTURE_SCORE|SEVERITY):\s*(.+)/i);
  if (scoreMatch) {
    const val = scoreMatch[1].trim();
    const num = parseInt(val);
    result.score = isNaN(num) ? val : num;
  }
  const summaryMatch = raw.match(/SUMMARY:\s*([\s\S]+?)(?=\n[A-Z_]+:|$)/);
  if (summaryMatch) {
    result.summary = summaryMatch[1].trim();
  }
  const sectionRegex = /^([A-Z][A-Z_]+):\s*$/gm;
  let match;
  const sectionPositions = [];
  while ((match = sectionRegex.exec(raw)) !== null) {
    const name = match[1];
    if (name === "SUMMARY") continue;
    sectionPositions.push({ name, index: match.index + match[0].length });
  }
  for (let i = 0; i < sectionPositions.length; i++) {
    const { name, index } = sectionPositions[i];
    const end = sectionPositions[i + 1]?.index ?? raw.length;
    const content = raw.slice(index, end).trim();
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
