const input = document.getElementById("postingInput");
const charCount = document.getElementById("charCount");
const analyzeBtn = document.getElementById("analyzeBtn");
const btnText = document.getElementById("btnText");
const btnLoading = document.getElementById("btnLoading");
const resultsSection = document.getElementById("resultsSection");
const resultsInner = document.getElementById("resultsInner");

// Char counter
input.addEventListener("input", () => {
  const len = input.value.length;
  charCount.textContent = `${len.toLocaleString()} character${len !== 1 ? "s" : ""}`;
  charCount.style.color = len > 50 ? "rgba(168,85,247,0.7)" : "rgba(255,255,255,0.25)";
});

function setLoading(on) {
  analyzeBtn.disabled = on;
  btnText.style.display = on ? "none" : "inline";
  btnLoading.style.display = on ? "inline" : "none";
}

function getVerdictClass(verdict) {
  if (!verdict) return "suspicious";
  const v = verdict.toUpperCase();
  if (v.includes("LIKELY SCAM") || v.includes("SCAM")) return "scam";
  if (v.includes("SUSPICIOUS")) return "suspicious";
  if (v.includes("CAUTION")) return "caution";
  if (v.includes("LEGITIMATE") || v.includes("LEGIT")) return "legit";
  return "suspicious";
}

function getVerdictIcon(cls) {
  if (cls === "scam")   return "🚨";
  if (cls === "suspicious") return "⚠️";
  if (cls === "caution") return "🟡";
  return "✅";
}

function renderResults(analysis) {
  const cls = getVerdictClass(analysis.verdict);
  const icon = getVerdictIcon(cls);
  const score = analysis.scam_score ?? 0;

  const redFlags = analysis.red_flags || [];
  const signals  = analysis.legitimacy_signals || [];
  const missing  = analysis.missing_info || [];

  let html = `
    <!-- Score card -->
    <div class="score-card ${cls}">
      <div class="score-top">
        <div class="score-left">
          <div class="verdict-badge ${cls}">${icon} ${analysis.verdict || "UNKNOWN"}</div>
          <p class="verdict-summary">${analysis.verdict_summary || ""}</p>
        </div>
        <div class="score-meter-wrap">
          <div class="score-circle ${cls}">
            <span class="score-num">${score}</span>
            <span class="score-label">/ 100</span>
          </div>
          <div class="score-meter-label">Scam Risk Score</div>
        </div>
      </div>
    </div>
  `;

  // Red flags
  if (redFlags.length > 0) {
    html += `
      <div class="result-section">
        <div class="result-section-title red">🚩 Red Flags Detected (${redFlags.length})</div>
        ${redFlags.map(f => `
          <div class="flag-item">
            <span class="flag-severity ${(f.severity || "medium").toLowerCase()}">${f.severity || "MEDIUM"}</span>
            <div class="flag-body">
              <div class="flag-name">${f.flag}</div>
              <div class="flag-explanation">${f.explanation}</div>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  } else {
    html += `
      <div class="result-section">
        <div class="result-section-title green">✅ No Red Flags Detected</div>
        <p style="color:var(--text-mid);font-size:0.9rem;">This posting passed all scam pattern checks.</p>
      </div>
    `;
  }

  // Legitimacy signals
  if (signals.length > 0) {
    html += `
      <div class="result-section">
        <div class="result-section-title green">✅ Legitimacy Signals (${signals.length})</div>
        ${signals.map(s => `
          <div class="signal-item">
            <span class="signal-dot">✦</span>
            <div class="signal-body">
              <div class="signal-name">${s.signal}</div>
              <div class="signal-explanation">${s.explanation}</div>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  }

  // Recommendation
  if (analysis.recommendation) {
    html += `
      <div class="result-section">
        <div class="result-section-title blue">💡 Recommendation</div>
        <p class="recommendation-text">${analysis.recommendation}</p>
      </div>
    `;
  }

  // Missing info
  if (missing.length > 0) {
    html += `
      <div class="result-section">
        <div class="result-section-title orange">📋 Missing Information</div>
        <div class="missing-list">
          ${missing.map(m => `<span class="missing-tag">${m}</span>`).join("")}
        </div>
      </div>
    `;
  }

  resultsInner.innerHTML = html;
  resultsSection.style.display = "flex";
  setTimeout(() => resultsSection.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
}

async function analyzePosting() {
  const text = input.value.trim();
  if (!text || text.length < 30) {
    input.style.borderColor = "#EF4444";
    input.focus();
    setTimeout(() => input.style.borderColor = "", 1500);
    return;
  }

  setLoading(true);
  resultsSection.style.display = "none";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }
    if (data.success && data.analysis) {
      renderResults(data.analysis);
    }
  } catch (err) {
    alert("Something went wrong. Please try again.");
    console.error(err);
  } finally {
    setLoading(false);
  }
}

// Allow Ctrl+Enter to submit
input.addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") analyzePosting();
});
