from google import genai
from typing import Dict

class StockAnalyzer:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def analyze_qualitative(self, ticker: str, business_text: str, mda_text: str, risk_text: str) -> str:
        # prompt = f"""
        # Analyze the following sections from the latest 10-K filing of {ticker}.
        # Provide a rating for each of the FOUR categories below using this scale:
        # [Excellent / Strong / Adequate / Weak / Poor] (for the first three)
        # [Minimal / Manageable / Moderate / High / Existential] (for Risk Profile)

        # ### RATING DEFINITIONS:

        # **1. Durable Competitive Advantages (Moat)**
        # - **Excellent**: Wide moat. Irreplaceable brand, massive network effects, or significant cost advantages. High switching costs.
        # - **Strong**: Notable moat. Strong brand recognition or scale advantages. High barriers to entry.
        # - **Adequate**: Some advantage. Competitive in its niche, but faces constant pressure. Moderate barriers to entry.
        # - **Weak**: Low advantage. Commodity-like product/service. Price is the primary competition.
        # - **Poor**: No advantage. Losing market share or being disrupted by new entrants.

        # **2. Reinvestment Opportunities**
        # - **Excellent**: Abundant high-return opportunities. Can reinvest most cash flow into projects with very high ROIC.
        # - **Strong**: Consistent high-return opportunities. Can reinvest a significant portion of cash into profitable growth.
        # - **Adequate**: Moderate opportunities. Can grow with the market, but high-return projects are limited.
        # - **Weak**: Few opportunities. Market is saturated; reinvestment mostly for maintenance.
        # - **Poor**: No opportunities. Industry is in decline; reinvestment is value-destructive.

        # **3. Management Capability**
        # - **Excellent**: Visionary and shareholder-aligned. Outstanding capital allocation history. Highly transparent.
        # - **Strong**: Capable and aligned. Good strategic execution and sensible capital allocation.
        # - **Adequate**: Competent. Follows industry standards, but lacks exceptional vision in capital allocation.
        # - **Weak**: Questionable alignment or strategy. Poor capital allocation choices (e.g., expensive M&A).
        # - **Poor**: Incompetent or misaligned. History of value destruction or lack of integrity.

        # **4. Risk Profile**
        # - **Minimal**: Low operational or financial risk. Highly stable environment.
        # - **Manageable**: Typical industry risks that are well-mitigated.
        # - **Moderate**: Significant risks exist (e.g., regulatory, technological) but are currently under control.
        # - **High**: Severe threats to the business model or financial stability.
        # - **Existential**: The company faces risks that could lead to insolvency or total disruption.

        # ---
        # BUSINESS SECTION (PARTIAL):
        # {business_text[:20000]}

        # MANAGEMENT DISCUSSION & ANALYSIS (PARTIAL):
        # {mda_text[:20000]}

        # RISK FACTORS (PARTIAL):
        # {risk_text[:20000]}
        # ---

        # OUTPUT FORMAT:
        # For each category, provide the RATING followed by a concise JUSTIFICATION based on the text provided.
        # """

        prompt = f"""
        Analyze the following sections from the latest 10-K filing of {ticker}.

        Provide a rating for each of the FOUR categories below using this scale:
        [Excellent / Strong / Adequate / Weak / Poor] (for the first three)
        [Minimal / Manageable / Moderate / High / Existential] (for Risk Profile)

        Then identify THREE concrete business-breaking scenarios based strictly on the filing.

        ### RATING DEFINITIONS:

        1. Durable Competitive Advantages (Moat)
        - Excellent: Wide moat. Irreplaceable brand, dominant network effects, or structural cost advantages. High switching costs.
        - Strong: Clear competitive advantages with meaningful barriers to entry.
        - Adequate: Some advantages, but faces persistent competitive pressure.
        - Weak: Limited differentiation. Competes largely on price or execution.
        - Poor: No durable advantage. Losing share or structurally disadvantaged.

        2. Reinvestment Opportunities
        - Excellent: Large and expanding TAM with sustained high-ROIC reinvestment potential.
        - Strong: Clear growth runway with attractive incremental returns.
        - Adequate: Growth in line with industry; limited high-return expansion.
        - Weak: Few scalable reinvestment opportunities.
        - Poor: Industry stagnation or value-destructive reinvestment.

        3. Management Capability
        - Excellent: Exceptional capital allocators with long-term orientation and strong alignment.
        - Strong: Demonstrated strategic clarity and disciplined allocation.
        - Adequate: Competent operators but limited evidence of superior capital allocation.
        - Weak: Inconsistent strategy or questionable capital decisions.
        - Poor: Value-destructive allocation or misaligned incentives.

        4. Risk Profile
        - Minimal: Highly stable model with limited operational or financial vulnerabilities.
        - Manageable: Typical industry risks, well-acknowledged and mitigated.
        - Moderate: Significant risks that could impair performance if triggered.
        - High: Severe strategic, regulatory, technological, or financial exposure.
        - Existential: Realistic risk of insolvency, disruption, or permanent impairment.

        ---

        5. THESIS-BREAKING SCENARIOS (Critical Section)

        Identify THREE specific scenarios that could materially impair or permanently damage the business.

        For each scenario:
        - Describe the triggering condition
        - Explain the mechanism of damage
        - Assess whether management appears aware/prepared
        - Classify severity: [Serious / Severe / Existential]

        Focus on structural risks such as:
        - Technological disruption
        - Regulatory change
        - Customer concentration
        - Platform dependency
        - Capital allocation failure
        - Margin compression from competition
        - Balance sheet fragility

        Avoid generic statements. Tie scenarios explicitly to the text provided.

        ---

        BUSINESS SECTION (PARTIAL):
        {business_text[:20000]}

        MANAGEMENT DISCUSSION & ANALYSIS (PARTIAL):
        {mda_text[:20000]}

        RISK FACTORS (PARTIAL):
        {risk_text[:20000]}

        ---

        OUTPUT FORMAT:

        1. Durable Competitive Advantages: [RATING]
        Justification: ...

        2. Reinvestment Opportunities: [RATING]
        Justification: ...

        3. Management Capability: [RATING]
        Justification: ...

        4. Risk Profile: [RATING]
        Justification: ...

        5. Thesis-Breaking Scenarios:
        Scenario 1:
        Trigger:
        Mechanism:
        Management Preparedness:
        Severity:

        Scenario 2:
        ...

        Scenario 3:
        ...
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error during analysis: {str(e)}"
