# qscanner Roadmap 🗺️

`qscanner` is currently in **Phase 2 (Enhanced Analysis)**, transitioning toward advanced features.

## ✅ Phase 1: MVP (Complete)
- [x] Ticker-to-CIK resolution.
- [x] Automatic 10-K retrieval from SEC EDGAR.
- [x] Robust HTML section extraction (Items 1, 1A, and 7).
- [x] AI-powered qualitative analysis via Gemini API.
- [x] Ordinal/Categorical rating system with defined anchors.
- [x] Security-first environment variable configuration.

## ✅ Phase 2: Enhanced Analysis (Complete)
- [x] **Multi-year Comparison**: Compare filings across multiple years to identify trends in management's tone or strategy.
- [x] **Forensic Adversarial Prompting**: Detection of structural decay, management bias, and strategic drift.
- [x] **SEC Rate-Limiting**: Built-in throttling (10 req/s) and retry logic to avoid 429 errors.
- [x] **History Inspection**: New `check-filings` command to see available data before analysis.

## 🚧 Phase 3: Advanced Features (Active)
- [ ] **Financial Integration**: Pull key financial ratios (ROIC, Net Margin, Debt/Equity) to support the qualitative analysis.
- [ ] **Local Caching**: Cache SEC filings locally to reduce bandwidth and speed up repeated runs.
- [ ] **Section Extraction Improvements**: Refine the parser to handle more diverse 10-K HTML layouts from smaller companies.

## 🚀 Phase 4: Future Expansion (Planned)
- [ ] **Competitor Benchmarking**: Compare two tickers side-by-side using their latest filings.
- [ ] **Earnings Call Integration**: Pull and analyze transcript data from the most recent earnings call for real-time management sentiment.
- [ ] **PDF/Markdown Export**: Save generated reports for offline reading and research tracking.
- [ ] **Web Dashboard**: A simple UI to visualize the qualitative ratings over time.

---

### Current Status: 🟩 Active Development
The core engine is stable and uses `gemini-2.5-flash` for high-speed, forensic-grade qualitative evaluation.
