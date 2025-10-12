"""
LLM integration module using Ollama for compliance analysis.
"""
import json
from typing import List, Dict, Optional
import ollama


class ComplianceLLM:
    """LLM-based compliance checker using Ollama."""
    
    def __init__(self, model_name: str = 'llama3.2'):
        """
        Initialize compliance LLM.
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        
    def check_compliance(self, prospectus_text: str, regulatory_context: List[str], 
                        check_type: str) -> Dict:
        """
        Check compliance of prospectus text against regulatory requirements.
        
        Args:
            prospectus_text: Text from the prospectus to check
            regulatory_context: List of relevant regulatory text chunks
            check_type: Type of compliance check (fee_disclosure, risk_disclosure, etc.)
            
        Returns:
            Dictionary with compliance analysis results
        """
        prompt = self._build_compliance_prompt(
            prospectus_text, 
            regulatory_context, 
            check_type
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a regulatory compliance expert specializing in Hong Kong investment fund regulations. Analyze documents for compliance violations with precision and cite specific regulatory requirements.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            result = self._parse_response(response['message']['content'], check_type)
            return result
            
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return {
                'violation_found': False,
                'error': str(e)
            }
    
    def _build_compliance_prompt(self, prospectus_text: str, 
                                 regulatory_context: List[str], 
                                 check_type: str) -> str:
        """Build prompt for compliance checking."""
        
        check_instructions = {
            'fee_disclosure': """
Check if the prospectus text contains COMPLETE fee disclosure including:
- Management fees (percentage and calculation method)
- Performance fees (if applicable, with calculation methodology)
- Administrative expenses and other charges
- Clear examples or illustrations of fee calculations
            """,
            'risk_disclosure': """
Check if the prospectus text contains ADEQUATE risk disclosures including:
- Market risk (volatility, market conditions)
- Liquidity risk (ability to sell holdings)
- Currency risk (for foreign investments or multi-currency share classes)
- Specific risk factors relevant to the investment strategy
            """,
            'concentration_limits': """
Check if the prospectus text mentions investment concentration limits:
- Single issuer exposure limits (typically 10% maximum)
- Sector concentration restrictions
- Geographic diversification requirements
- Compliance with investment restrictions
            """
        }
        
        regulatory_text = "\n\n---\n\n".join(regulatory_context)
        
        prompt = f"""You are analyzing an investment fund prospectus for compliance with Hong Kong regulations.

COMPLIANCE CHECK TYPE: {check_type}

REGULATORY REQUIREMENTS:
{regulatory_text}

PROSPECTUS EXCERPT TO ANALYZE:
{prospectus_text}

INSTRUCTIONS:
{check_instructions.get(check_type, 'Analyze for general compliance issues.')}

Provide your analysis in the following format:

VIOLATION: [YES/NO]
SEVERITY: [CRITICAL/WARNING/NONE]
ISSUE: [Brief description of the specific compliance issue, or "No violation found"]
REGULATION_CITATION: [Specific section or requirement violated, or "N/A"]
EXPLANATION: [Detailed explanation of why this is or is not a violation]

Be specific and cite actual regulatory requirements. If no violation is found, clearly state that.
"""
        return prompt
    
    def _parse_response(self, response_text: str, check_type: str) -> Dict:
        """Parse LLM response into structured format."""
        
        result = {
            'violation_found': False,
            'severity': 'NONE',
            'issue': '',
            'regulation_citation': '',
            'explanation': '',
            'check_type': check_type,
            'raw_response': response_text
        }
        
        lines = response_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('VIOLATION:'):
                violation_status = line.split(':', 1)[1].strip().upper()
                result['violation_found'] = 'YES' in violation_status
            elif line.startswith('SEVERITY:'):
                result['severity'] = line.split(':', 1)[1].strip().upper()
                if result['severity'] not in ['CRITICAL', 'WARNING', 'NONE']:
                    result['severity'] = 'WARNING' if result['violation_found'] else 'NONE'
            elif line.startswith('ISSUE:'):
                result['issue'] = line.split(':', 1)[1].strip()
            elif line.startswith('REGULATION_CITATION:'):
                result['regulation_citation'] = line.split(':', 1)[1].strip()
            elif line.startswith('EXPLANATION:'):
                result['explanation'] = line.split(':', 1)[1].strip()
        
        return result
