# qscanner 🔍

`qscanner` is a high-performance CLI tool for performing deep qualitative analysis on U.S. stocks. It bypasses expensive financial data providers by pulling directly from the SEC's EDGAR database and uses free/low-cost Gemini AI models to evaluate business quality.

## 🚀 Features

- **Automated Data Sourcing**: Resolves Tickers to SEC CIKs and fetches filings directly from SEC EDGAR.
- **Smart Section Extraction**: Isolates key qualitative sections: Item 1 (Business), Item 1A (Risk Factors), and Item 7 (MD&A).
- **Adversarial Multi-Year Analysis**: Tracks business consistency, detects structural decay, and flags management bias across multiple years.
- **Forensic Quality Assessment**: Evaluates Moat Durability, Strategic Discipline, Risk Escalation, and Capital Allocation Quality.
- **Throttled SEC Access**: Built-in rate limiting (10 requests/sec) to comply with SEC guidelines.
- **Rich CLI Experience**: Interactive help, descriptive parameters, and beautiful terminal formatting powered by `rich`.

## ⚖️ Scoring Framework (Forensic)

The multi-year analysis uses a strict burden of proof to classify businesses:

- **Pristine**: Clear durable moat, disciplined capital allocation, stable strategy, low risk creep.
- **High**: Durable business with manageable risks and consistent execution.
- **Moderate**: Mixed signals, unclear durability, or capital discipline concerns.
- **Speculative**: Weak moat evidence, strategy drift, elevated risk.
- **Deteriorating**: Structural decay, capital destruction, increasing operational strain.

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/onglichang/qscanner.git
   cd qscanner
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

## ⚙️ Configuration

The tool requires two environment variables:

```bash
# Get your key at https://aistudio.google.com/
export GEMINI_API_KEY="your_api_key_here"

# The SEC requires a User-Agent header for identification
export SEC_USER_AGENT="Your Name yourname@email.com"
```

## 📈 Usage

You can always run `qscanner --help` to see the latest commands and options.

### 1. Check Available History
See how many years of 10-K filings are available for a ticker:
```bash
qscanner check-filings MSFT
```

### 2. Deep Qualitative Analysis (Latest Filing)
Analyze the most recent 10-K for a single-year snapshot:
```bash
qscanner analyze AAPL
```

### 3. Forensic Multi-Year Analysis
Analyze consistency and quality over a specified number of years (default is 3):
```bash
qscanner multi-analyze GOOGL --years 5
# or using the short flag
qscanner multi-analyze GOOGL -y 5
```

---
*Disclaimer: This tool is for educational and research purposes only. It is not financial advice.*
