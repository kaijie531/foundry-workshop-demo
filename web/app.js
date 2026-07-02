// Sentiment Analyzer — the visible web app shipped by the agentic pipeline.
// Ship features by editing this file: a PR runs CI, the Foundry agent reviews
// it, a human approves, it merges, and GitHub Pages redeploys the live site.

const POSITIVE = ["good", "great", "love", "excellent", "amazing", "happy", "best", "brilliant", "fantastic", "fabulous"];
const NEGATIVE = ["bad", "terrible", "hate", "awful", "worst", "sad", "poor"];

function analyze(text) {
  const words = text.toLowerCase().split(/\s+/).map((w) => w.replace(/[.,!?;:]/g, ""));
  const positive = words.filter((w) => POSITIVE.includes(w)).length;
  const negative = words.filter((w) => NEGATIVE.includes(w)).length;
  const score = (positive - negative) / Math.max(words.length, 1);
  let label = "neutral";
  if (score > 0) label = "positive";
  else if (score < 0) label = "negative";
  return { label, score: Math.round(score * 1000) / 1000 };
}

function render() {
  const text = document.getElementById("input").value.trim();
  const el = document.getElementById("result");
  if (!text) {
    el.className = "result hidden";
    return;
  }
  const { label, score } = analyze(text);
  const emoji = { positive: "😀", negative: "🙁", neutral: "😐" }[label];
  el.className = `result ${label}`;
  el.innerHTML = `<div class="emoji">${emoji}</div><div class="label">${label}</div><div class="score">score: ${score}</div>`;
}

document.getElementById("analyze").addEventListener("click", render);
document.getElementById("input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) render();
});
