
import re
from src.qscanner.utils import extract_section

# specific test case simulating a 10-K structure
mock_10k = """
UNITED STATES SECURITIES AND EXCHANGE COMMISSION
Form 10-K

Table of Contents
Item 1. Business ....................... 4
Item 1A. Risk Factors .................. 12
Item 7. Management's Discussion ........ 35

PART I

Item 1. Business.
General
We are a technology company...
(This is the actual content we want)

Item 1A. Risk Factors.
Investing in our stock involves risks...
"""

print("--- TESTING ITEM 1 EXTRACTION ---")
extracted = extract_section(mock_10k, "Item 1", "Item 1A")
print(f"Extracted Length: {len(extracted)}")
print(f"Snippet: {extracted[:100]}...")

if "We are a technology company" in extracted:
    print("SUCCESS: Found actual content.")
else:
    print("FAILURE: Likely caught Table of Contents.")
