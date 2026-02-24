import requests
import json
from typing import Dict, Optional
from rich.console import Console

console = Console()

class SECClient:
    def __init__(self, user_agent: str):
        self.headers = {'User-Agent': user_agent}
        self.ticker_map: Dict[str, str] = {}
        self._load_ticker_map()

    def _load_ticker_map(self):
        """Loads ticker to CIK mapping from SEC."""
        url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            # The JSON format is like {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
            for entry in data.values():
                ticker = entry['ticker'].upper()
                # Pad CIK to 10 digits
                cik = str(entry['cik_str']).zfill(10)
                self.ticker_map[ticker] = cik
        else:
            raise Exception(f"Failed to fetch ticker map: {response.status_code}")

    def get_cik(self, ticker: str) -> Optional[str]:
        return self.ticker_map.get(ticker.upper())

    def get_latest_10k_url(self, cik: str) -> Optional[str]:
        """Gets the URL for the most recent 10-K filing."""
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = requests.get(submissions_url, headers=self.headers)
        if response.status_code != 200:
            return None

        data = response.json()
        recent_filings = data.get('filings', {}).get('recent', {})
        
        # Loop through filings to find the latest '10-K'
        for i, form in enumerate(recent_filings.get('form', [])):
            if form == '10-K':
                accession_number = recent_filings['accessionNumber'][i].replace('-', '')
                primary_document = recent_filings['primaryDocument'][i]
                return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
        
        return None

    def fetch_filing_content(self, url: str) -> str:
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        console.print("Filing content empty")
        return ""
