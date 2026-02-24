
from src.qscanner.sec_client import SECClient
from src.qscanner.utils import clean_html, extract_section
import os

def debug_extraction():
    user_agent = os.getenv("SEC_USER_AGENT", "qscanner/1.0 (contact@example.com)")
    client = SECClient(user_agent)
    ticker = "AAPL"
    cik = client.get_cik(ticker)
    print(f"CIK: {cik}")
    
    url = client.get_latest_10k_url(cik)
    print(f"URL: {url}")
    
    html = client.fetch_filing_content(url)
    print(f"HTML Length: {len(html)}")
    
    full_text = clean_html(html)
    print(f"Clean Text Length: {len(full_text)}")
    
    # Save a snippet of the clean text to see what it looks like
    with open("debug_full_text.txt", "w") as f:
        f.write(full_text[:50000]) # first 50k chars

    biz = extract_section(full_text, "Item 1", "Item 1A")
    mda = extract_section(full_text, "Item 7", "Item 7A")
    
    print(f"Biz Length: {len(biz)}")
    print(f"Biz Snippet: {biz[:200]}...")
    
    print(f"MDA Length: {len(mda)}")
    print(f"MDA Snippet: {mda[:200]}...")

if __name__ == "__main__":
    debug_extraction()
