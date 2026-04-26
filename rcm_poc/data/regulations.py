"""
Sample Regulatory Data
Simulates scraped regulations from regulator websites (FCA, PRA, Basel, etc.)
"""

SAMPLE_REGULATIONS = [
    {
        "id": "REG-2025-FCA-001",
        "title": "Prudential Regulation - SS2/25: Consumer Duty Enhancements",
        "regulator": "FCA",
        "date": "19 December 2025",
        "type": "Supervisory Statement",
        "source_url": "https://www.fca.org.uk/publications/ss2-25",
        "full_text": """
        SS2/25: Consumer Duty Enhancements - Prudential Considerations

        1. INTRODUCTION
        This supervisory statement sets out the PRA's expectations regarding the implementation
        of enhanced consumer duty requirements for retail banking institutions.

        2. APPLICABILITY
        This statement applies to all PRA-authorised firms offering retail banking products
        including personal current accounts, savings products, mortgages, and personal loans.
        Firms with total retail deposits exceeding £1 billion are subject to enhanced requirements.

        3. KEY MANDATES
        3.1 Fair Value Assessment
        Firms must conduct quarterly fair value assessments across all retail product lines.
        The assessment must demonstrate that the price paid by consumers is reasonable relative
        to the overall benefits received, including non-financial benefits.

        3.2 Consumer Understanding
        All product communications must achieve a minimum Flesch-Kincaid readability score of 60.
        Firms must implement consumer testing protocols for new product launches and material
        changes to existing products.

        3.3 Consumer Support Standards
        Firms must ensure support channels are accessible to consumers with characteristics
        of vulnerability. Response times for complaints must not exceed 3 business days.
        All frontline staff must complete Consumer Duty training within 6 months.

        3.4 Governance Requirements
        Boards must receive quarterly Consumer Duty MI packs. A nominated Consumer Duty Champion
        at Board level is required. Annual Consumer Duty assessments must be submitted to the FCA.

        4. COMPLIANCE TIMELINE
        - Immediate: Begin fair value assessments for all existing products
        - 3 months: Consumer testing protocols operational
        - 6 months: Staff training complete
        - 12 months: Full governance framework operational

        5. PENALTIES
        Non-compliance may result in regulatory action including financial penalties up to
        £10 million or 10% of annual turnover, whichever is greater.
        """,
        "mandates": [
            "Quarterly fair value assessments for all retail products",
            "Consumer communications readability score minimum 60 (Flesch-Kincaid)",
            "Consumer testing for new product launches",
            "Complaint response within 3 business days",
            "Consumer Duty training for all frontline staff within 6 months",
            "Quarterly Consumer Duty MI reporting to Board",
            "Nominated Consumer Duty Champion at Board level",
            "Annual Consumer Duty assessment submission to FCA"
        ]
    },
    {
        "id": "REG-2026-PRA-001",
        "title": "Prudential Regulation - Basel IV Capital Requirements",
        "regulator": "PRA",
        "date": "02 January 2026",
        "type": "Policy Statement",
        "source_url": "https://www.bankofengland.co.uk/prudential-regulation/publication/2026/basel-iv",
        "full_text": """
        PS1/26: Implementation of Basel IV Capital Requirements

        1. OVERVIEW
        This policy statement finalises the PRA's rules implementing the Basel III.1 standards
        (commonly referred to as Basel IV) in the UK. These rules significantly revise the
        calculation of risk-weighted assets (RWAs) for credit risk, operational risk, and market risk.

        2. APPLICABILITY
        Applies to all PRA-authorised banks and building societies. Enhanced requirements apply
        to firms with total assets exceeding £50 billion (Large firms).

        3. CREDIT RISK CHANGES
        3.1 Standardised Approach Revisions
        - Removal of reliance on external credit ratings for certain exposures
        - New risk weight for unrated corporate exposures: 100% (previously 100% with ratings relief)
        - Residential mortgage risk weights recalibrated based on LTV bands
        - Retail exposure definition tightened: max £1 million per obligor

        3.2 IRB Approach Restrictions
        - Input floor of 5% applied to PD estimates for retail mortgages
        - LGD floors: 10% for residential mortgages, 15% for other retail
        - Removal of advanced IRB for financial institutions and large corporates

        4. OPERATIONAL RISK
        New Business Indicator (BI) approach replaces Advanced Measurement Approach (AMA).
        Internal Loss Multiplier (ILM) applies to firms with BI above £1 billion.

        5. OUTPUT FLOOR
        72.5% output floor on RWAs relative to Standardised Approach applies from 2028.
        Transitional arrangements: 50% in 2025, 55% in 2026, 60% in 2027.

        6. REPORTING REQUIREMENTS
        Enhanced COREP reporting templates from Q1 2026.
        Annual ICAAP must reflect Basel IV methodology by December 2026.
        """,
        "mandates": [
            "Recalculate credit RWAs under revised Standardised Approach",
            "Apply IRB input floors: 5% PD for retail mortgages",
            "Apply LGD floors: 10% residential mortgage, 15% other retail",
            "Implement Business Indicator operational risk calculation",
            "Apply 50% output floor on RWAs from 2025",
            "Update COREP reporting templates by Q1 2026",
            "Revise ICAAP to reflect Basel IV methodology by December 2026",
            "Remove advanced IRB for financial institutions and large corporates"
        ]
    },
    {
        "id": "REG-2025-FCA-LIAF03",
        "title": "Policy Statement - LIAF03: Liquidity & Funding Requirements",
        "regulator": "FCA",
        "date": "19 December 2025",
        "type": "Policy Statement",
        "source_url": "https://www.fca.org.uk/publications/liaf03",
        "full_text": """
        LIAF03: Enhanced Liquidity and Funding Requirements for Investment Firms

        1. BACKGROUND
        Following the review of liquidity stress events in 2024, the FCA is introducing
        enhanced liquidity requirements for investment firms under IFPR.

        2. SCOPE
        Applies to UK Investment Firms (SNI and non-SNI) authorised under the Investment
        Firms Prudential Regime (IFPR).

        3. LIQUID ASSET BUFFER (LAB)
        3.1 SNI Firms: Minimum LAB of £10,000 (unchanged)
        3.2 Non-SNI Firms: LAB must cover minimum 1 month of fixed overheads
        3.3 New stress scenarios must be applied: 30-day, 90-day, and 180-day horizons
        3.4 LAB composition: minimum 80% in Level 1 HQLA assets

        4. WIND-DOWN PLANNING
        All non-SNI firms must maintain an updated Wind-Down Plan (WDP).
        WDP must demonstrate ability to wind-down within 12 months.
        Board approval of WDP annually required.

        5. INTRADAY LIQUIDITY
        Firms must monitor intraday liquidity positions daily.
        Peak intraday exposure must be reported in ICARA.

        6. REPORTING
        Monthly liquidity returns (FSA047/048) for non-SNI firms with AUM > £5bn.
        Quarterly liquidity stress test results to be submitted to FCA.
        """,
        "mandates": [
            "Maintain Liquid Asset Buffer covering 1 month fixed overheads (non-SNI)",
            "Apply 30-day, 90-day, 180-day liquidity stress scenarios",
            "Ensure minimum 80% of LAB in Level 1 HQLA assets",
            "Maintain Board-approved Wind-Down Plan updated annually",
            "Demonstrate 12-month wind-down capability in WDP",
            "Monitor and report intraday liquidity positions daily",
            "Submit monthly FSA047/048 returns (non-SNI AUM > £5bn)",
            "Submit quarterly liquidity stress test results to FCA"
        ]
    }
]

BANK_PROFILES = {
    "HSBC": {
        "name": "HSBC Bank plc",
        "type": "Global Universal Bank",
        "jurisdiction": "UK",
        "total_assets": "£2.1 trillion",
        "retail_deposits": "£450 billion",
        "products_services": {
            "Personal Banking": ["Current Accounts", "Savings & Term Deposits", "Credit Cards", "Mortgages", "Personal Loans", "Customer Tiers (Advance, Premier, Premier Elite)"],
            "Wealth Management": ["Investments", "Insurance", "Financial Advice"],
            "Business Banking": ["Commercial Accounts", "Business Current Accounts", "HSBC Kinetic", "Financing", "Corporate Cards"],
            "Trade Finance": ["Letters of Credit", "Receivables Finance", "Supply Chain Finance"],
            "Global Liquidity": ["Multi-border cash management solutions"]
        },
        "policies": [
            "Consumer Duty Policy (CDP-001)",
            "Credit Risk Management Policy (CRM-001)",
            "Operational Risk Framework (ORF-001)",
            "Liquidity Risk Policy (LRP-001)",
            "Capital Management Policy (CAP-001)",
            "Conduct Risk Policy (CON-001)"
        ],
        "internal_controls": [
            "IC-001: Fair Value Assessment Control",
            "IC-002: Consumer Communication Review",
            "IC-003: Complaint Handling Process",
            "IC-004: Staff Training & Competency",
            "IC-005: RWA Calculation Engine",
            "IC-006: Liquidity Monitoring Dashboard",
            "IC-007: COREP Reporting Control",
            "IC-008: Board MI Reporting"
        ],
        "regulators": ["FCA", "PRA", "Basel Committee"]
    },
    "Barclays": {
        "name": "Barclays Bank UK plc",
        "type": "Universal Bank",
        "jurisdiction": "UK",
        "total_assets": "£1.5 trillion",
        "retail_deposits": "£290 billion",
        "products_services": {
            "Personal Banking": ["Current Accounts", "Savings", "Mortgages", "Credit Cards", "Personal Loans"],
            "Premier Banking": ["Barclays Premier", "Private Bank"],
            "Business Banking": ["Business Accounts", "Merchant Services", "Trade Finance"],
            "Investment Banking": ["Corporate Finance", "Markets", "Research"]
        },
        "policies": [
            "Consumer Duty & Conduct Policy (CDP-BAR-001)",
            "Credit Risk Policy (CRP-BAR-001)",
            "Market Risk Framework (MRF-BAR-001)",
            "Operational Resilience Policy (ORP-BAR-001)",
            "Capital Adequacy Policy (CAP-BAR-001)"
        ],
        "internal_controls": [
            "IC-BAR-001: Product Fair Value Review",
            "IC-BAR-002: Consumer Outcome Testing",
            "IC-BAR-003: Capital Calculation Control",
            "IC-BAR-004: Liquidity Stress Testing",
            "IC-BAR-005: Regulatory Reporting Control"
        ],
        "regulators": ["FCA", "PRA"]
    },
    "Lloyds": {
        "name": "Lloyds Banking Group plc",
        "type": "Retail & Commercial Bank",
        "jurisdiction": "UK",
        "total_assets": "£920 billion",
        "retail_deposits": "£380 billion",
        "products_services": {
            "Personal Banking": ["Current Accounts", "Savings", "Mortgages", "Personal Loans", "Credit Cards"],
            "Insurance": ["Home Insurance", "Life Insurance", "Car Insurance"],
            "Commercial Banking": ["SME Banking", "Mid-Market", "Global Corporates"],
            "Wealth": ["Scottish Widows", "Financial Planning"]
        },
        "policies": [
            "Consumer Duty Implementation Policy",
            "Credit Risk Management Policy",
            "Conduct Risk Policy",
            "Capital & Liquidity Policy",
            "Operational Risk Policy"
        ],
        "internal_controls": [
            "IC-LBG-001: Consumer Duty Monitoring",
            "IC-LBG-002: Mortgage Risk Weight Calculation",
            "IC-LBG-003: Liquidity Coverage Ratio",
            "IC-LBG-004: ICAAP Control Framework",
            "IC-LBG-005: Regulatory MI Production"
        ],
        "regulators": ["FCA", "PRA"]
    }
}
