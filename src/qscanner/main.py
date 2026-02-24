import typer
import os
from rich.console import Console
from rich.panel import Panel
from .sec_client import SECClient
from .analyzer import StockAnalyzer
from .utils import clean_html, extract_section

app = typer.Typer()
console = Console()

@app.command()
def analyze(ticker: str):
    """
    Analyze a stock qualitatively using SEC filings.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]Error: GEMINI_API_KEY not found in environment.[/red]")
        raise typer.Exit(code=1)

    user_agent = os.getenv("SEC_USER_AGENT", "qscanner/1.0 (contact@example.com)")
    
    with console.status(f"[bold green]Fetching data for {ticker}...") as status:
        client = SECClient(user_agent)
        cik = client.get_cik(ticker)
        if not cik:
            console.print(f"[red]Ticker {ticker} not found.[/red]")
            return

        url = client.get_latest_10k_url(cik)
        if not url:
            console.print(f"[red]Could not find latest 10-K for {ticker}.[/red]")
            return

        html_content = client.fetch_filing_content(url)
        full_text = clean_html(html_content)
        
        # Extract sections
        business_section = extract_section(full_text, "Item 1", "Item 1A")
        risk_section = extract_section(full_text, "Item 1A", "Item 1B")
        mda_section = extract_section(full_text, "Item 7", "Item 7A")

    with console.status("[bold green]Analyzing with Gemini...") as status:
        analyzer = StockAnalyzer(api_key)
        report = analyzer.analyze_qualitative(ticker, business_section, mda_section, risk_section)

    console.print(Panel(report, title=f"Qualitative Analysis: {ticker}", expand=False))

if __name__ == "__main__":
    app()
