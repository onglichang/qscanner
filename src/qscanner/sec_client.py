import requests
import json
import time
from typing import Dict, Optional
from rich.console import Console

console = Console()

class SECClient:
    def __init__(self, user_agent: str):
        self.headers = {'User-Agent': user_agent}
        self.ticker_map: Dict[str, str] = {}
        self._last_request_time = 0.0
        self._min_delay = 0.11  # 10 requests per second limit (0.1s), using 0.11s for safety
        self._load_ticker_map()

    def _make_request(self, url: str) -> requests.Response:
        """Throttled GET request to comply with SEC rate limits."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_delay:
            time.sleep(self._min_delay - elapsed)
        
        response = requests.get(url, headers=self.headers)
        self._last_request_time = time.time()
        
        if response.status_code == 429:
            console.print("[yellow]SEC Rate limit hit. Retrying after delay...[/yellow]")
            time.sleep(10)  # Standard cool-off
            return self._make_request(url)
            
        return response

    def _load_ticker_map(self):
        """Loads ticker to CIK mapping from SEC."""
        url = "https://www.sec.gov/files/company_tickers.json"
        response = self._make_request(url)
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

    def get_available_10ks(self, cik: str) -> list[str]:
        """Returns a list of filing dates for all available 10-K filings."""
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = self._make_request(submissions_url)
        if response.status_code != 200:
            return []

        data = response.json()
        filings = data.get('filings', {})
        recent_filings = filings.get('recent', {})
        
        filing_dates = []
        
        def extract_from_dict(d):
            for i, form in enumerate(d.get('form', [])):
                if form == '10-K':
                    filing_dates.append(d['filingDate'][i])

        # Extract from recent
        extract_from_dict(recent_filings)
        
        # Extract from older files if they exist
        older_files = filings.get('files', [])
        for file_info in older_files:
            file_name = file_info.get('name')
            if file_name:
                file_url = f"https://data.sec.gov/submissions/{file_name}"
                file_response = self._make_request(file_url)
                if file_response.status_code == 200:
                    extract_from_dict(file_response.json())
        
        # Sort dates descending
        filing_dates.sort(reverse=True)
        return filing_dates

    def get_10k_urls(self, cik: str, limit: int = 3) -> list[Dict[str, str]]:
        """Returns a list of URLs and dates for the most recent 10-K filings up to the limit."""
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = self._make_request(submissions_url)
        if response.status_code != 200:
            return []

        data = response.json()
        filings_data = []
        
        def extract_filings(d):
            for i, form in enumerate(d.get('form', [])):
                if form == '10-K':
                    accession_number = d['accessionNumber'][i].replace('-', '')
                    primary_document = d['primaryDocument'][i]
                    date = d['filingDate'][i]
                    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
                    filings_data.append({"date": date, "url": url})

        # Recent filings
        extract_filings(data.get('filings', {}).get('recent', {}))
        
        # Older filings if needed
        if len(filings_data) < limit:
            older_files = data.get('filings', {}).get('files', [])
            for file_info in older_files:
                if len(filings_data) >= limit: break
                file_name = file_info.get('name')
                if file_name:
                    file_url = f"https://data.sec.gov/submissions/{file_name}"
                    file_res = self._make_request(file_url)
                    if file_res.status_code == 200:
                        extract_filings(file_res.json())

        # Sort by date descending and take the limit
        filings_data.sort(key=lambda x: x['date'], reverse=True)
        return filings_data[:limit]

    def get_latest_10k_url(self, cik: str) -> Optional[str]:
        """Gets the URL for the most recent 10-K filing."""
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = self._make_request(submissions_url)
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
        response = self._make_request(url)
        if response.status_code == 200:
            return response.text
        console.print("Filing content empty")
        return ""
