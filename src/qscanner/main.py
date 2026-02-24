import typer
import os
from typing import Annotated
from rich.console import Console
from rich.panel import Panel
from .sec_client import SECClient
from .analyzer import StockAnalyzer
from .utils import clean_html, extract_section

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command()
def analyze(
    ticker: Annotated[
        str, 
        typer.Argument(
            help="The stock ticker symbol to analyze (e.g. AAPL).",
            show_default=False
        )
    ]
):
    """
    Perform a deep qualitative analysis of the LATEST 10-K filing.
    
    Evaluates Moat, Reinvestment, Management, and Risk based on the most recent submission.
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

@app.command()
def check_filings(
    ticker: Annotated[
        str, 
        typer.Argument(
            help="The stock ticker to check for available filings (e.g. MSFT).",
            show_default=False
        )
    ]
):
    """
    List all available 10-K filing dates for a given ticker.
    
    Useful for seeing how far back the historical data goes before running a multi-year analysis.
    """
    user_agent = os.getenv("SEC_USER_AGENT", "qscanner/1.0 (contact@example.com)")
    client = SECClient(user_agent)
    cik = client.get_cik(ticker)
    if not cik:
        console.print(f"[red]Ticker {ticker} not found.[/red]")
        return

    filing_dates = client.get_available_10ks(cik)
    if not filing_dates:
        console.print(f"[yellow]No 10-K filings found for {ticker}.[/yellow]")
        return

    console.print(f"[bold green]Found {len(filing_dates)} years of 10-K filings for {ticker}:[/bold green]")
    for date in filing_dates:
        console.print(f" - {date}")

@app.command()
def multi_analyze(
    ticker: Annotated[
        str, 
        typer.Argument(
            help="The stock ticker to analyze (e.g. GOOGL).",
            show_default=False
        )
    ],
    years: Annotated[
        int, 
        typer.Option(
            "--years", "-y",
            help="Number of historical years to include in the analysis."
        )
    ] = 3
):
    """
    Perform a forensic, multi-year analysis to track business consistency and decay.
    
    This adversarial analysis detects structural deterioration, strategy drift, 
    and management bias across multiple years of 10-K filings.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]Error: GEMINI_API_KEY not found in environment.[/red]")
        raise typer.Exit(code=1)

    user_agent = os.getenv("SEC_USER_AGENT", "qscanner/1.0 (contact@example.com)")
    client = SECClient(user_agent)
    
    with console.status(f"[bold green]Identifying {years} years of filings for {ticker}...") as status:
        cik = client.get_cik(ticker)
        if not cik:
            console.print(f"[red]Ticker {ticker} not found.[/red]")
            return

        filings_info = client.get_10k_urls(cik, limit=years)
        if not filings_info:
            console.print(f"[red]Could not find 10-K filings for {ticker}.[/red]")
            return

    filings_content = []
    for info in filings_info:
        date = info['date']
        url = info['url']
        with console.status(f"[bold blue]Fetching and processing {date} filing...") as status:
            html_content = client.fetch_filing_content(url)
            full_text = clean_html(html_content)
            
            # Extract sections
            business_section = extract_section(full_text, "Item 1", "Item 1A")
            risk_section = extract_section(full_text, "Item 1A", "Item 1B")
            mda_section = extract_section(full_text, "Item 7", "Item 7A")
            
            filings_content.append({
                "date": date,
                "business": business_section,
                "mda": mda_section,
                "risk": risk_section
            })

    with console.status(f"[bold green]Performing longitudinal analysis of {len(filings_content)} years...") as status:
        analyzer = StockAnalyzer(api_key)
        report = analyzer.analyze_multi_year(ticker, filings_content)

    console.print(Panel(report, title=f"Multi-Year Quality Analysis: {ticker}", expand=False))

if __name__ == "__main__":
    app()
