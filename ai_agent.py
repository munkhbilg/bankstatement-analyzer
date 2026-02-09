import google.generativeai as genai
import os
import json
import re
from typing import Dict, Any

class FinancialAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def structure_data(self, extracted_text: str) -> Dict[str, Any]:
        """Structure extracted text into JSON format with better prompting"""
        
        prompt = f"""
        Дараах банкны хуулгын текстийг шинжилж, JSON форматруу зөв оруул.
        Analyze the following Mongolian bank statement text and structure it into a valid JSON format.
        Extract the following information:
        - bank_name (string)
        - account_holder (string)
        - statement_period (string)
        - transactions (array of objects with: date, description, amount, type)
        - opening_balance (number)
        - closing_balance (number)

        TEXT TO ANALYZE:
        {extracted_text}

        Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            json_text = self._extract_json_from_response(response.text)
            structured_data = json.loads(json_text)
            
            # Post-process to ensure numeric amounts
            return self._ensure_numeric_amounts(structured_data)
            
        except Exception as e:
            print(f"AI structuring failed: {e}")
            return self._fallback_structure(extracted_text)
    
    def _ensure_numeric_amounts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all amount fields are numbers, not strings"""
        if 'transactions' in data:
            for transaction in data['transactions']:
                if 'amount' in transaction and isinstance(transaction['amount'], str):
                    # Remove currency symbols and convert to float
                    cleaned = re.sub(r'[^\d.-]', '', transaction['amount'])
                    try:
                        transaction['amount'] = float(cleaned)
                    except (ValueError, TypeError):
                        transaction['amount'] = 0.0
        
        balance_fields = ['opening_balance', 'closing_balance', 'total_deposits', 'total_withdrawals']
        for field in balance_fields:
            if field in data and isinstance(data[field], str):
                cleaned = re.sub(r'[^\d.-]', '', data[field])
                try:
                    data[field] = float(cleaned)
                except (ValueError, TypeError):
                    data[field] = 0.0
        
        return data
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """Extract JSON from AI response"""
        # Look for JSON pattern
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_candidate = response_text[start_idx:end_idx]
            # Basic validation
            if json_candidate.count('{') == json_candidate.count('}'):
                return json_candidate
        
        import re
        json_match = re.search(r'\{[^{}]*\{[^{}]*\}[^{}]*\}', response_text)
        if json_match:
            return json_match.group()
        
        return '{"bank_name": "Unknown", "transactions": []}'
    
    def _fallback_structure(self, text: str) -> Dict[str, Any]:
        """Fallback structure when AI fails"""
        return {
            "bank_name": "Unknown",
            "account_holder": "Unknown",
            "statement_period": "Unknown",
            "transactions": [],
            "opening_balance": 0,
            "closing_balance": 0,
            "raw_text": text[:1000] 
        }