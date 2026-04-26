"""
RCM AI Agent - Core Intelligence Engine
Implements: Applicability Check → Impact Assessment → Gap Analysis → Recommendations
Uses Anthropic Claude API via agentic RAG pattern
"""

import anthropic
import json
from typing import Optional


class RCMAnalystAgent:
    """
    AI-powered Regulatory Change Management Analyst Agent.
    Mirrors the Gap Analyzer Agent from the Logical View architecture.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        self.model = "claude-sonnet-4-20250514"

    def check_applicability(self, regulation: dict, bank_profile: dict) -> dict:
        """
        Step 2: Triage & Applicability Review
        Determine if a regulation applies to the bank and which business units are in scope.
        """
        prompt = f"""You are an expert Regulatory Change Management (RCM) analyst at a major UK bank.

BANK PROFILE:
Name: {bank_profile['name']}
Type: {bank_profile['type']}
Jurisdiction: {bank_profile['jurisdiction']}
Total Assets: {bank_profile.get('total_assets', 'N/A')}
Retail Deposits: {bank_profile.get('retail_deposits', 'N/A')}
Products & Services: {json.dumps(bank_profile['products_services'], indent=2)}
Regulators: {', '.join(bank_profile.get('regulators', []))}

REGULATION:
ID: {regulation['id']}
Title: {regulation['title']}
Regulator: {regulation['regulator']}
Type: {regulation['type']}
Date: {regulation['date']}

Full Regulation Text:
{regulation['full_text']}

TASK: Perform a detailed applicability assessment. Return ONLY valid JSON with this exact structure:
{{
  "is_applicable": true/false,
  "applicability_score": 0-100,
  "applicability_rationale": "detailed explanation",
  "in_scope_business_units": ["list of business units that are in scope"],
  "out_of_scope_business_units": ["list of business units not in scope"],
  "key_applicability_criteria": ["criteria that make this applicable or not"],
  "compliance_timeline": {{"immediate": "actions needed now", "short_term": "0-6 months", "medium_term": "6-12 months"}},
  "assigned_sme": ["SME functions that should own this"],
  "regulatory_risk_rating": "High/Medium/Low",
  "rationale_for_rating": "why this risk rating"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        # Extract JSON
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])

    def perform_impact_assessment(self, regulation: dict, bank_profile: dict, applicability: dict) -> dict:
        """
        Step 3: Impact Assessment & Gap Analysis
        Identify impact on policies and internal controls.
        """
        prompt = f"""You are an expert RCM Impact Assessment analyst.

BANK: {bank_profile['name']}

EXISTING POLICIES:
{json.dumps(bank_profile['policies'], indent=2)}

EXISTING INTERNAL CONTROLS:
{json.dumps(bank_profile['internal_controls'], indent=2)}

REGULATION MANDATES:
{json.dumps(regulation['mandates'], indent=2)}

FULL REGULATION TEXT:
{regulation['full_text']}

APPLICABILITY CONTEXT:
In-Scope Business Units: {json.dumps(applicability.get('in_scope_business_units', []))}
Risk Rating: {applicability.get('regulatory_risk_rating', 'Medium')}

TASK: Perform a detailed impact assessment of this regulation on the bank's policies and controls.
Return ONLY valid JSON:
{{
  "overall_impact_level": "High/Medium/Low",
  "impact_summary": "executive summary of overall impact",
  "policy_impacts": [
    {{
      "policy_name": "name of affected policy",
      "impact_type": "New/Amend/No Change",
      "impact_description": "what needs to change",
      "mandates_triggering": ["which regulation mandates trigger this"],
      "effort_estimate": "High/Medium/Low",
      "priority": 1
    }}
  ],
  "control_impacts": [
    {{
      "control_name": "name of affected control",
      "impact_type": "New/Strengthen/Retire/No Change",
      "current_state": "description of current control",
      "required_state": "description of what control needs to become",
      "gap_description": "the gap between current and required",
      "mandates_triggering": ["which mandates trigger this"],
      "effort_estimate": "High/Medium/Low",
      "priority": 1
    }}
  ],
  "new_controls_required": [
    {{
      "control_name": "name of new control needed",
      "control_description": "what this control must do",
      "mandate_triggering": "which mandate requires this",
      "implementation_complexity": "High/Medium/Low"
    }}
  ],
  "risks_if_non_compliant": ["list of risks if not compliant"],
  "estimated_total_effort": "weeks/months estimate"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])

    def generate_action_plan(self, regulation: dict, bank_profile: dict,
                              applicability: dict, impact: dict) -> dict:
        """
        Step 4: Actionable Gaps / Recommendations
        Generate a prioritised action plan for remediation.
        """
        prompt = f"""You are an expert RCM Remediation Planner.

BANK: {bank_profile['name']}
REGULATION: {regulation['title']} ({regulation['id']})
COMPLIANCE DEADLINE: {applicability.get('compliance_timeline', {})}

POLICY GAPS:
{json.dumps(impact.get('policy_impacts', []), indent=2)}

CONTROL GAPS:
{json.dumps(impact.get('control_impacts', []), indent=2)}

NEW CONTROLS REQUIRED:
{json.dumps(impact.get('new_controls_required', []), indent=2)}

TASK: Create a detailed, prioritised action plan. Return ONLY valid JSON:
{{
  "executive_summary": "brief exec summary",
  "total_actions": 0,
  "critical_actions": [
    {{
      "action_id": "ACT-001",
      "action_title": "title",
      "action_description": "detailed description of what to do",
      "action_type": "Policy Update/Control Enhancement/New Control/Training/Reporting",
      "owner": "who owns this action",
      "due_date": "when it must be done",
      "priority": "Critical/High/Medium/Low",
      "effort_days": 0,
      "dependencies": ["other action IDs this depends on"],
      "success_criteria": "how to know this is done"
    }}
  ],
  "implementation_roadmap": {{
    "phase_1_immediate": {{
      "label": "Immediate (0-30 days)",
      "actions": ["ACT-001"]
    }},
    "phase_2_short_term": {{
      "label": "Short Term (30-90 days)",
      "actions": []
    }},
    "phase_3_medium_term": {{
      "label": "Medium Term (90-180 days)",
      "actions": []
    }}
  }},
  "estimated_cost_impact": "£ range estimate",
  "resource_requirements": ["list of resources/skills needed"],
  "key_risks_to_delivery": ["risks that could delay implementation"]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])

    def generate_regulation_summary(self, regulation: dict) -> dict:
        """Generate plain English summary with mandate decomposition."""
        prompt = f"""You are an expert regulatory interpreter.

REGULATION:
Title: {regulation['title']}
Regulator: {regulation['regulator']}
Full Text:
{regulation['full_text']}

TASK: Provide a plain English interpretation. Return ONLY valid JSON:
{{
  "plain_english_summary": "2-3 sentence plain English summary",
  "key_themes": ["3-5 key themes"],
  "mandates": [
    {{
      "mandate_id": "M-001",
      "mandate_title": "short title",
      "mandate_text": "original text",
      "plain_english": "plain English explanation",
      "mandate_type": "Reporting/Capital/Conduct/Governance/Operational",
      "sub_mandates": ["sub-requirements if any"]
    }}
  ],
  "who_is_affected": "description of which firms are affected",
  "key_dates": {{"immediate": "", "short_term": "", "medium_term": ""}},
  "penalty_risk": "description of penalties for non-compliance"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])

    def run_full_analysis(self, regulation: dict, bank_profile: dict,
                          progress_callback=None) -> dict:
        """
        Run the complete E2E RCM analysis pipeline:
        1. Regulation Summary
        2. Applicability Check
        3. Impact Assessment
        4. Action Plan
        """
        results = {}

        if progress_callback:
            progress_callback(0.1, "📋 Generating regulation summary...")
        results['summary'] = self.generate_regulation_summary(regulation)

        if progress_callback:
            progress_callback(0.3, "🔍 Running applicability check...")
        results['applicability'] = self.check_applicability(regulation, bank_profile)

        if results['applicability'].get('is_applicable', False):
            if progress_callback:
                progress_callback(0.55, "📊 Performing impact assessment & gap analysis...")
            results['impact'] = self.perform_impact_assessment(
                regulation, bank_profile, results['applicability']
            )

            if progress_callback:
                progress_callback(0.80, "🎯 Generating action plan & recommendations...")
            results['action_plan'] = self.generate_action_plan(
                regulation, bank_profile, results['applicability'], results['impact']
            )
        else:
            results['impact'] = None
            results['action_plan'] = None

        if progress_callback:
            progress_callback(1.0, "✅ Analysis complete!")

        return results
